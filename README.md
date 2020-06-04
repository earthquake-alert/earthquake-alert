# Earthquake alert

🇯🇵| [🇺🇸](documents/README_en.md)

## tl;dr

気象庁、防災科研他から地震情報を取得し、フォーマットした情報をSNSなどの様々なプラットフォームに送信します。

## 📢送信可能なサービス(予定)

- Discode
- Slack
- LINE (フリーのオフィシャルアカウントには月々の送信条件あり)

## 💬細かい仕様

- 基本的に、画像を生成して送信する。画像内には最大震度、震源地、各地の震度などの情報を記載する。
- Pythonは基本的に動作が遅いため、緊急地震速報など速さが問われるものに関してはPythonから`nimpy`経由でNimを呼び出したい。

## 🔧依存関係のインストール

### Python

```bash
# pipが入っていることが前提
pip install pipenv

# pipenvで仮想環境上に依存関係をインストールする
pipenv install

# pipenvで依存関係が入った仮想環境を開く
pipenv shell

# もしくは、システム上に直接依存関係をインストール
pipenv install --system --deploy
```

## 🔰コーディングルール

- [Pythonのコーディングルール](documents/python_rule.md)
- [Nimのコーディングルール](documents/nim_rule.md)

## ⚖ライセンス

[MIT LICENCE](LICENSE)を使用しています。
