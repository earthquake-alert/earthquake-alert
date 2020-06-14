'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import time

from convert_areas import convert, convert_report
from json_operation import json_read
from filter import Filter


def test_convert():
    '''
    TEST
    '''
    db_file_path = 'src/external/area-code-database/src/areas.db'
    image_file_path = 'src/cache/images'
    earthquake = json_read('test/example/8.json')
    push = Filter('config/user_setting.json', 'src/cache')

    output = convert(earthquake, db_file_path, image_file_path)
    push.post_type_1(output)


def test_repot():
    '''
    report
    '''
    image_file_path = 'src/cache/images'
    earthquake = json_read('test/example/5.json')
    push = Filter('config/user_setting.json', 'src/cache')

    output = convert_report(earthquake, image_file_path)
    push.post_type_2(output)


if __name__ == "__main__":
    start = time.time()
    # test_convert()
    test_repot()
    elapsed_time = time.time() - start
    print(f'Time: {elapsed_time}[sec]')
