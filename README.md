# 概要
PythonのTUIフレームワークである`Textual`というものを使ってエージェント型AIチャットボットを作りました。

# 開発環境
VScodeのDevContainerを使用しました。コンテナ情報もリポジトリに含まれています。

Pythonのバージョンは3.12です。

# 準備
`pip install -r requirements.txt`

# デバッグ
`ptw --runner "textual run --dev app.py"`でデバッグできます。  

これで起動するとコード変更と同時にリフレッシュされ開発が楽になります。