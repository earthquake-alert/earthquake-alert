'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
from src.acquisition import AcquisitionJMA


def test_get():
    link = 'http://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml'
    save_directory = 'test/test_cache'
    jma = AcquisitionJMA(link, save_directory)

    jma.check()

    if jma.is_infomation:
        assert jma.nfomation == []

    if jma.is_report:
        assert jma.report == []

    jma.init_element()
