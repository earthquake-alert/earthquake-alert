'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import multiprocessing
import os
import time

try:
    from acquisition import AcquisitionJMA
    from convert_areas import convert, convert_report
    from convert_message import convert_xml_report, convert_xml_infomation
    from filter import Filter
except ModuleNotFoundError:
    from src.acquisition import AcquisitionJMA
    from src.convert_areas import convert, convert_report
    from src.convert_message import convert_xml_report, convert_xml_infomation
    from src.filter import Filter


def main():
    '''
    Perform an earthquake bulletin.
    By operating multiple processes, you can send data from the Japan Meteorological Agency or NIED.
    '''
    user_config_path = os.path.join('config', 'user_setting.json')
    cache_dir = os.path.join('src', 'cache')
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    post = Filter(user_config_path, cache_dir)

    jma_process = multiprocessing.Process(target=jma, args=(post, cache_dir))

    jma_process.start()


def jma(post: Filter, cache_dir: str):
    '''
    We will acquire the “seismic intensity report” and “information about the epicenter and seismic intensity”
    from the Japan Meteorological Agency and send them to various platforms.

    Args:
        post (Filter): An instance of Filter to send.
        cache_dir (str): The path to the cache directory.
    '''
    link = 'http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml'

    db_file_path = os.path.join('src', 'external', 'area-code-database', 'src', 'areas.db')
    image_cache_dir = os.path.join(cache_dir, 'images')
    if not os.path.isdir(image_cache_dir):
        os.makedirs(image_cache_dir)

    acquisition = AcquisitionJMA(link, cache_dir)
    while(True):  # pylint: disable=C0325
        acquisition.check()

        if acquisition.is_report:
            formated_report = convert_xml_report(acquisition.report, cache_dir)
            after_report = convert_report(formated_report, image_cache_dir)
            post.post_type_2(after_report)
        elif acquisition.is_infomation:
            formated_imfomation = convert_xml_infomation(acquisition.infomation)
            after_infomation = convert(formated_imfomation, db_file_path, image_cache_dir)
            post.post_type_1(after_infomation)

        acquisition.init_element()
        time.sleep(30)


if __name__ == "__main__":
    main()
