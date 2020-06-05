# 変数名の定義

## `create_image()`

- save_file_path
  - string
  - 生成した画像を保存するファイルパス。
- title
  - string
  - タイトル。震度速報や緊急地震速報など
- areas
  - エリア。

    ```json
    {
        "震度４": [
            "茨城県",
            "埼玉県",
            "東京都"
            ],
        "震度３": [
            "神奈川県",
            "群馬県",
            "栃木県"
        ]
    }
    ```

- explanation
  - 解説、説明など。2つのみ

    ```json
    [
        "~~:~~ごろ強い地震を観測しました。震度３以上が観測された地域は以下の通りです。",
        "この地震による津波の心配はありません。"
    ]
    ```

- max_seismic_intensity
  - string
  - 最大震度
- epicenter
  - string
  - 震源地
- magnitude
  - float
  - マグニチュード
  - 3.2, 4.8
