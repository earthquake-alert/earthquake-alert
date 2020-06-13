'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import json
from typing import Any


def json_read(json_file_path: str) -> Any:
    '''
    read json file.
    Args:
        json_file_path (str): json file path.
    Returns:
        Any: json body.
    '''
    with open(json_file_path, mode='r') as contents:
        json_body = json.load(contents)

    return json_body


def json_write(json_file_path: str, json_body: Any) -> None:
    '''
    save json file.
    Args:
        json_file_path (str): json file path.
        json_body (Any): json body.
    '''
    with open(json_file_path, mode='w') as contents:
        json.dump(json_body, contents, indent=4, ensure_ascii=False)
