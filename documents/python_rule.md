# Pythonのコーディングルール

## 静的解析

以下の静的解析を使用します。

- [Flake8](https://flake8.pycqa.org/en/latest/)
  - Python静的解析の代表格。PEP8（Pythonの書き方の規則）に沿ってチェックしてくれる。
- [Pylint](https://www.pylint.org/)
  - Pythonの静的解析の代表格2。Flake8より詳しい内容をチェックしてくれる。ハズ。
- [Mypy](http://www.mypy-lang.org/)
  - 型をチェックしてくれる。詳しくは[Typing](#typing)参照。

実行するには、toxを使用します。

```bash
# toxのインストール
pip install tox

# pipenvのインストール（ない場合）
pip install pipenv

# 実行
tox
```

## Typing

変数の型をわかりやすくするためにTyping(型ヒント)を使用します。

```python
def (earthquake: str, report_number: int) -> str:
    ...
```

詳しくは[公式ドキュメント](https://docs.python.org/ja/3/library/typing.html)を参照してください。

## Docstring

Docstringは関数などに加えるコメントのことです。
GoogleスタイルのDocstringを使用してください。ソースコード内の使用言語はすべて英語に統一します。

例:

```python
def (earthquake: str, report_number: int) -> str:
    '''
    関数についての説明文

    Args:
        引数の名前1 (引数の型): 引数の説明1
        引数の名前2 (引数の型): 引数の説明2

    Returns:
        戻り値の型: 戻り値の説明

    Raises:
        例外の名前: 例外の説明
    '''
```

## 統一

- シングルクォーテーション`'`で統一します。
- TestCodeを使い、TDD（テスト駆動開発）を心がけてください。

## Test

- TDD（テスト駆動開発）を使用する。
- [Pytest](https://docs.pytest.org/en/latest/contents.html)を使用する。

## 変数の命名規則

- 意味のある変数にしてください。
  - `data`などの広範囲の意味の単語は極力使用しないでください。
  - `a`, `i`などの単体のアルファベット変数は使用しないでください。
    - forなどで使用する場合、

        ```python
        # 意味のある変数にする
        for element in range(100):
            ...
        # ただループするだけの場合
        for _ in range(100):
            ...
        ```

  - 日本語のローマ字（`zisinn`, `saidai_sindo`）は使用しないでください。
  - なんの意味のない変数（`hoge`, `foo`）は使用しないでください。
- PEP8に沿った命名をしてください。
    |  対象  |           ルール           |     例      |
    | :----: | :------------------------: | :---------: |
    | クラス | 先頭大文字。大文字で区切る |   MyClass   |
    |  例外  | 先頭大文字。大文字で区切る |   MyError   |
    |  関数  |   小文字のスネークケース   | my_function |
    |  変数  |   小文字のスネークケース   | my_instance |
    |  定数  |   大文字のスネークケース   |  MY_CONST   |

## ライセンス表記

ソースコードの先頭に記述してください。

```python
'''
@author: Your name

Copyright (c) 2020 Earthquake alert
'''
```

## Pythonのバージョン

3.8.x
