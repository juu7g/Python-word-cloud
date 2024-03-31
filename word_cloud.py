"""
ワードクラウド作成
日本語解析にテキストマイニング
"""
from logging import getLogger, StreamHandler, Formatter, DEBUG
logger = getLogger(__name__)

import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Mecab用インポート
import MeCab
# wordcloud用インポート
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from wordcloud import WordCloud

import collections

class MyFrame(tk.Frame):
    """
    ビュークラス
    """
    def __init__(self, master) -> None:
        """
        コンストラクタ：画面作成
        """
        super().__init__(master)
        # フレーム作成(作図用)
        frm_canvas = tk.Frame(master)
        frm_canvas.pack()
        # ボタン作成(開く)
        self.btn_open = tk.Button(master, text='ファイル選択')
        self.btn_open.pack(side=tk.LEFT)
        # ボタン作成(保存)
        self.btn_save = tk.Button(master, text='画像を保存', state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT)
        # ボタン作成(１回使用単語)
        self.btn_once = tk.Button(master, text='１回使用単語', state=tk.DISABLED)
        self.btn_once.pack(side=tk.LEFT)
        # ボタン作成(ストップワードの入力)
        self.stopword = ""
        self.btn_stop_w = tk.Button(master, text='非表示単語指定', state=tk.DISABLED
                            , command=self.input_stopword)
        self.btn_stop_w.pack(side=tk.LEFT)
        # キャンバス作成
        self.create_canvas(frm_canvas)
        # コンテキストメニュー作成(貼り付けのみ)
        self.cmenu = tk.Menu(self, tearoff=False, font=('メイリオ', 11))   # メニュー作成
        self.cmenu.add_command(label='貼り付け', command=self.do_paste)   # 要素追加
    
    def set_my_ctr(self, my_ctr):
        """
        MyControlクラスの参照を設定
        Args:
            MyControl:  MyControlオブジェクト
        """
        self.my_ctr = my_ctr
        self.btn_open.config(command=self.my_ctr.load_text_form_file)
        self.btn_save.config(command=self.my_ctr.save_image)
        self.btn_once.config(command=self.my_ctr.show_once_words)

    def create_canvas(self, parent):
        """
        matplotlibで作成した図をTkinterで表示
        """
        # matplotlibのFigure作成
        fig = Figure(figsize=(8, 6))
        fig.set_layout_engine('constrained')    # 隙間をなくすためレイアウトエンジンを指定
        # ワードクラウド用Axesを作成
        self.ax = fig.add_subplot(111)  # Axesを作成
        self.ax.set_axis_off()          # 軸を非表示
        # ワードクラウド用キャンバス作成
        self.canvas = FigureCanvasTkAgg(fig, parent)
        self.canvas.get_tk_widget().pack()

    def show_cmenu(self, event):
        """
        コンテキストメニュー表示
        """
        self.cmenu.post(event.x_root, event.y_root)

    def do_paste(self, event=None):
        """
        ペースト処理
        """
        text = self.clipboard_get()     # クリップボードから文字列取得
        self.my_ctr.create_wordcloud(text)

    def input_stopword(self, event=None):
        s = simpledialog.askstring('非表示単語指定', '表示したくない単語をカンマ区切りで入力してください', initialvalue=self.stopword)
        if s == None: return    # キャンセルの場合は何もせず戻る
        self.stopword = s
        self.my_ctr.view_word_cloud(s)

class MyModel():
    """
    モデルクラス
    """
    def __init__(self) -> None:
        """
        コンストラクタ
        """
        pass

    def load_text_file(self):
        """
        テキストファイルの読み込み(ファイル選択ダイアログ表示)
        """
        self.text = ""
        paths = filedialog.askopenfilenames(
                filetypes=[("テキスト", ".txt"), ("md", ".md"), ("すべて", "*")])
        if paths:
            for path in paths:
                try:
                    with open(path, encoding='utf-8') as f:
                        self.text += f.read()
                except UnicodeDecodeError as e:
                    try:
                        with open(path, encoding='shift_jis') as f:
                            self.text += f.read()
                    except UnicodeDecodeError as e:
                        pass         # エンコードエラーをはじく テキストファイル以外も

class MyControl():
    """
    コントロールクラス
    """

    def __init__(self, model:MyModel, view:MyFrame) -> None:
        """
        コンストラクタ
        Args:
            MyModel:    モデルのオブジェクト
            MyFrame:    ビューのオブジェクト
        """
        self.model = model  # モデルオブジェクト
        self.view = view    # ビューオブジェクト

    def create_wordcloud(self, text:str):
        """
        """        
        if not text: return
        self.words = self.create_wakachigaki(text)
        self.view_word_cloud()
        self.view.btn_save.config(state=tk.NORMAL)  # ボタンを有効にする
        self.view.btn_once.config(state=tk.NORMAL)  # ボタンを有効にする
        self.view.btn_stop_w.config(state=tk.NORMAL)  # ボタンを有効にする
        # 調査
        if logger.isEnabledFor(DEBUG):
            self.check_hinshi()

    def create_wakachigaki(self, text:str):
        """
        テキストマイニング
        """
        tagger = MeCab.Tagger() # 
        tokens = tagger.parse(text)
        self.all_tokens = [l.split() for l in tokens.splitlines()]
        logger.debug(self.all_tokens)
        logger.info(f"　全単語数：{len(self.all_tokens)}")
        # 品詞が名詞と形容詞のものだけを抽出。英数字を省く
        # tokens = [s[0] for s in tokens if len(s) > 3 and s[4].startswith('名詞') and re.match(r"[^a-zA-Z0-9\W]+", s[0])]
        tokens = [s[0] for s in self.all_tokens if len(s) > 3 and re.match('名詞|形容詞|接頭辞|接尾辞', s[4]) and re.match(r"[^a-zA-Z0-9\W]+", s[0])]
        logger.info(f"抽出単語数：{len(tokens)}")
        logger.debug(tokens)
        logger.debug(collections.Counter(tokens).most_common(10))
        return tokens

    def view_word_cloud(self, stopwords:str=""):
        """
        ワードクラウド生成    generateであれば単語の出現頻度も調べる
        Args:
            str:    非表示ワード(カンマ区切り)
        """
        self.wc = WordCloud(font_path="meiryo.ttc"   # 日本語フォントを指定
                    , background_color="white"
                    , max_words=50              # 出力する単語数
                    , width=800
                    , height=400
                    # , relative_scaling=1
                    # , regexp=r"[^a-zA-Z0-9\W]+" # 単語の抽出条件
                    , collocations=False        # 連語の連結
                    , stopwords=set(stopwords.split(','))    # {"こと", "ため", "ない"}
                    # , min_word_length=1        # 最低文字長の指定
                    )        # 最低文字長の指定
        self.wc.generate(" ".join(self.words))           # 日本語の単語を空白でつなげて渡す

        # ワードクラウドをAxesに追加
        self.view.ax.imshow(self.wc, interpolation="bilinear")
        self.view.canvas.draw()
    
    def save_image(self, event=None):
        """
        ワードクラウドを画像ファイルに保存
        """
        path = filedialog.asksaveasfilename(filetypes=[("イメージ", "*.png")])
        if path and hasattr(self, 'wc'):
            self.wc.to_file(path)

    def load_text_form_file(self, event=None):
        """
        ファイルからテキストデータを取得
        """
        self.model.load_text_file()
        self.create_wordcloud(self.model.text)
    
    def show_once_words(self, event=None):
        """
        一回使用単語をダイアログ表示
        """
        logger.info(f"一回使用単語抽出前単語数：{len(self.all_tokens)}")
        # 英数字を省く。一文字を除く
        tokens = [s[0] for s in self.all_tokens if re.match(r"[^a-zA-Z0-9\W]+", s[0]) and len(s[0]) > 1]
        c = collections.Counter(tokens)
        words = [w for w, count in c.items() if count == 1]
        logger.info(f"一回使用単語抽出後単語数：{len(words)}")
        words.sort()
        messagebox.showinfo("１回使用単語", "\t".join(words))

    def check_hinshi(self):
        """
        品詞チェック チェック結果はloggerに出力
        """
        # 品詞だけを抽出
        tokens = [re.sub("-.+", "", s[4]) for s in self.all_tokens if len(s) > 3]
        c = collections.Counter(tokens)
        logger.debug(c.most_common(20))
        # 気になる単語の品詞チェック
        tokens = [(s[0], s[4]) for s in self.all_tokens if len(s) > 3 and s[0]== 'お']
        c = collections.Counter(tokens)
        logger.debug(c.most_common())

class App(tk.Tk):
    """
    アプリケーションクラス
    """
    def __init__(self) -> None:
        """
        コンストラクタ：操作画面クラスと制御クラスを作成し関連付ける
        """
        super().__init__()

        self.title("ワードクラウド")      # タイトル

        my_model = MyModel()

        my_frame = MyFrame(self)                # MyFrameクラス(V)のインスタンス作成
        my_frame.pack()

        # ペーストの設定
        self.bind('<Control-v>', my_frame.do_paste)
        self.bind('<Button-3>', my_frame.show_cmenu)    # 右クリックでコンテキストメニュー表示

        my_ctr = MyControl(my_model, my_frame)  # 制御クラス(C)のインスタンス作成
        my_frame.set_my_ctr(my_ctr)             # ビューにMyControlクラスを設定

if __name__ == '__main__':
    # logger setting
    LOGLEVEL = "INFO"   # ログレベル('CRITICAL','FATAL','ERROR','WARN','WARNING','INFO','DEBUG','NOTSET')
    logger = getLogger()
    handler = StreamHandler()	# このハンドラーを使うとsys.stderrにログ出力
    handler.setLevel(LOGLEVEL)
    logger.setLevel(LOGLEVEL)
    # ログ出形式を定義 時:分:秒.ミリ秒 L:行 M:メソッド名 T:スレッド名 コメント
    if logger.isEnabledFor(DEBUG):
        handler.setFormatter(Formatter("{asctime}.{msecs:.0f} {name} L:{lineno:0=3} T:{threadName} M:{funcName} : {message}", "%H:%M:%S", "{"))
    logger.addHandler(handler)
    logger.propagate = False
    logger.debug("start log")

    app = App()
    app.mainloop()
