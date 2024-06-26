# Python-word-cloud

## 概要 Description
ワードクラウド  
テキストデータを単語に分解して使用頻度の高い単語を大きく表示してランダムに並べて表示します。

## 特徴 Features

- テキストファイルを指定してワードクラウドを作成  
	複数ファイル指定可能
- 文字列をコピーアンドペーストしてワードクラウドを作成
- 作成されたワードクラウドから非表示にしたい単語を指定し再作成
- テキストをテキストマイニング後、一度しか使用されていない単語を表示
- ワードクラウドを画像に保存可能
- 出力単語数を設定可能

## 依存関係 Requirement

- Python 3.8.5
- mecab-python3 1.0.8
- unidic-lite 1.0.8
- wordcloud 1.9.3

## 操作方法 Method of operation

### ワードクラウドの作成
- 【ファイル選択して作成】
	1. 「ファイル選択」ボタンを押す
	1. ファイル選択ダイアログが出るのでファイルを選択  
		ファイルは一つでも複数でも選択可能です
	1. ダイアログを閉じると結果を表示します
- 【コピペして作成】
	1. テキストを選択してコピー  
		コピペ可能なテキストであれば何でも構いません
	1. アプリ画面で右クリックして「貼り付け」を選択
	1. 貼り付け後、結果を表示します

### ワードクラウド結果の保存
1. 「画像を保存」ボタンを押す
1. ファイルダイアログが出るのでファイル名を指定  
	拡張子も指定。拡張子に合わせた画像で保存します

### １回使用単語の表示
一度しか使用していない単語は誤字の可能性があります。  
ブログ記事を書いた時に簡単にチェックできればと用意しました。  

1. 「１回使用単語」ボタンを押す
1. ダイアログに１回使用単語を表示します
1. 「OK」ボタンを押すと閉じます

### 非表示単語指定
現在表示しているワードクラウドを見て、結果に反映して欲しくない単語を指定してワードクラウドを再作成できます。

1. 「非表示単語指定」ボタンを押します
1. 文字入力ダイアログが出るので非表示にしたい単語を入力します  
	複数の単語を入力する場合、「,」（半角カンマ）で区切ります  
	例：「`こと,ない`」
1. 「OK」ボタンを押すか Enter でワードクラウドを再作成します

## 操作画面 Operation screen
- ファイル選択ボタン　：ファイル選択ダイアログでテキストファイルを選択します
- 画像を保存ボタン　　：作成されたワードクラウドを画像として保存します
- １回使用単語ボタン　：一度しか使用されていない単語をダイアログで列挙します
- 非表示単語指定ボタン：非表示にしたい単語を指定します
- 出力単語数　　　　　：出力する単語の最大数を指定します

## 制限事項  

- テキストファイルの文字コードは「UTF-8」と「Shift-JIS」のものだけを処理します
- 半角の英数字と記号は読み飛ばします
- テキストは品詞付与の結果、名詞、形容詞、接頭辞、接尾辞を対象にします

## プログラムの説明サイト Program description site

- 使い方：[単語の使用頻度をワードクラウドで表示するアプリ【フリー】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/word-cloud-exe)  
- 作り方：[単語の使用頻度をワードクラウドで表示するアプリの作り方【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/word-cloud)  
  
## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSEファイルを確認してください。  
This software is released under the MIT License, see LICENSE file.

