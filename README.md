# Earthquake alert

🇯🇵| [🇺🇸](documents/README_en.md)

## tl;dr

- 気象庁、防災科研他から地震情報を取得し、フォーマットした情報をSNSなどのさまざまなプラットフォームに送信します。
- 震度分布図を作成します。 (´-ω-｀)

## 📢 送信可能なプラットフォーム

- Discode（サーバーウェブフック）
- Slack（Slack bot）
- LINE（LINE notify）

## 💬 細かい仕様

- 震度速報はテンプレートを適用した画像のみ。震源・震度に関する情報はテンプレートを適用した画像と震度分布図を送信します。
- 複数のプラットフォームに別々に「送信する最低震度」「対象地域」を指定できます。
- Dcokerですべて動作させるため、デプロイ時に他の依存関係をインストールする必要はありません。

## 🚀 動かす

**Git、Dockerがインストールされていることが前提です。**

必ず、git経由でダウンロードをしてください。

```bash
git clone https://github.com/earthquake-alert/earthquake-alert.git
```

[chrome-driver](#-chrome-driverについて)のバージョンを確認して、任意で最新版Chromeに対応したものへ変更してください。

```bash
# サブモジュールのアップデート
sh build/init_submodule.sh

# 動かす
docker-compose up -d

# ログの確認
docker-compose logs -f

# 一時停止
docker-compose stop

# 再開
docker-compose up -d

# 停止(コンテナも削除)
docker-compose down
```

## ⚠ chrome driverについて

Chromeは最新版をビルドする際に取得します。そのため、chrome-driverは常に最新版Chromeに合ったバージョンである必要があります。\
以下のサイトから最新版に対応したchrome-driverのダウンロードリンクをコピーして、[Dockerfil](./Dockerfile)eの`install ChromeDriver`部分の**ADD**内のリンクを変更してください。

[Index of chrome-driver](https://chromedriver.storage.googleapis.com/index.html)

## 📝 設定ファイルの書き方

設定ファイルは、Docker containerと同期しています。\
新しく設定を追加する場合は`docker-compose stop`で一時停止してから追加してください。\
新しく追加または変更された場合は最初に、各プラットフォームに設定が送信されます。

[設定ファイルの書き方](documents/hou_to_setting.md)

## 🔰 コーディングルール

[Pythonのコーディングルール](documents/python_rule.md)

## ⚖ ライセンス

[MIT LICENSE](LICENSE)
