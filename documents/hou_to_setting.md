# 設定ファイルの書き方

ユーザーは任意で送信するプラットフォームの設定できます。

[config/user_setting.json](../config/user_setting.json)

を変更してください。

例:

```json
{
    "push_discord": {
        "platform": 3,
        "token": "[Token]",
        "seismic_intensity": "0",
        "areas": [],
        "is_quick_report": true
    },
    "push_line": {
        "platform": 1,
        "token": "[Token]",
        "seismic_intensity": "3",
        "areas": [
            "茨城県",
            "埼玉県",
            "東京都"
        ],
        "is_quick_report": false
    },
    "push_slack": {
        "platform": 2,
        "token": "[Token]",
        "channel": "#general",
        "seismic_intensity": "3",
        "areas": [],
        "is_quick_report": false
    },
    "push_twitter": {
        "platform": 4,
        "consumer_key": "[consumer key]",
        "consumer_secret": "[consumer secret]",
        "token": "[Token]",
        "token_secret": "[token secret]",
        "seismic_intensity": "0",
        "areas": [],
        "is_quick_report": false
    }
}
```

- 指定する個別の要素は以下のように記述します。
  - `名前`は送信されません。

```json
"[名前]" : {
    ...
}
```

- 個別の要素の中の説明
  - `platform`
    - 送信するプラットフォームを指定します。
      - 1:LINEnotify, 2:Slack, 3:Discord
    - 1から3の整数を入れてください。
  - `token`
    - アクセストークンまたはWebhookURLを指定してください。
  - `seismic_intensity`
    - 送信する最大震度の最低値を指定します。
    - `1, 2, 3, 4, 5-, 5+, 6-, 6+, 7`で指定してください。
    - 必ずstr型で指定してください。
    - `0`の場合、すべての震度の情報を送信します。
  - `areas`
    - 送信する地震の都道府県を指定します。
    - 必ず、都道府県をつけてください。例: `東京都`
    - からのリスト`[]`の場合はすべての地域の情報を送信します。
  - `is_quick_report`
    - 緊急速報を送信します。
    - **現実未実装なため設定しても何も起きません。**
  - `channel`
    - **Slackのみです。他で指定しても意味はありません。**
    - Slackの送信するチャンネルを指定します。
  - `consumer_key`
    - **Twitterのみです。他で指定しても意味はありません。**
    - TwitterAPIのコンシューマキー
  - `consumer_secret`
    - **Twitterのみです。他で指定しても意味はありません。**
    - TwitterAPIのコンシューマシークレットキー
  - `token_secret`
    - **Twitterのみです。他で指定しても意味はありません。**
    - TwitterAPIのシークレットトークン
