'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import Any, List

import requests
import xmltodict

try:
    from json_operation import json_write, json_read  # pyright: reportMissingImports=false
except ModuleNotFoundError:
    from src.json_operation import json_write, json_read

# Too many variables and instance is specifications
# pylint: disable=R0914
# pylint: disable=R0902


class AcquisitionJMA():
    '''
    Obtain the latest "Information on the epicenter
    and intensity of the earthquake" and "Seismic intensity bulletin" from JMA XML telegrams.
    '''

    def __init__(self, link: str, save_directory: str):
        '''
        Initialization

        Args:
            link (str): JMA xml message link.
            save_directory (str): directory in save cache file.
        '''
        self.link = link
        self.save_directory = save_directory
        self.save_file_path = os.path.join(self.save_directory, 'JMA_cache.json')
        self.__creaet_directory()
        self.responce = None

        self.is_infomation = False        # Information about the epicenter and intensity.
        self.infomation: List[str] = []   # Same as above

        self.is_report = False            # Seismic intensity bulletin.
        self.report: List[str] = []       # Same as above

    def init_element(self):
        '''
        Initialize a specific element.
        '''
        self.is_infomation = False
        self.infomation = []
        self.is_report = False
        self.report = []

    def __creaet_directory(self):
        '''
        if directory is not exist, created it.
        '''
        if not os.path.isdir(self.save_directory):
            os.makedirs(self.save_directory)

    def check(self):
        '''
        Refer to the header information on the JMA website and check if the message has been updated.

        If it has been updated,
        We will compare the "information about the epicenter
        and "the seismic intensity" and the "seismic intensity preliminary report" with those obtained last time.
        '''
        try:
            self.responce = requests.get(self.link)
        except requests.exceptions.ConnectionError:
            return

        last_acquisition = self.__load_cache({'latest': None, 'report': [], 'infomation': []})

        try:
            last_modified = self.responce.headers['Last-Modified']
        except KeyError:
            return

        if last_modified != last_acquisition['latest']:
            delete_ids = set()
            report_ids = set(last_acquisition['report'])
            infomation_ids = set(last_acquisition['infomation'])

            self.responce.encoding = 'UTF-8'
            xml_data = self.responce.text

            try:
                text = xmltodict.parse(xml_data)
            except xmltodict.expat.ExpartError:
                return

            for element in text['feed']['entry']:
                title = element['title']
                _id = element['id']
                if title == '震度速報' and _id not in report_ids:
                    url = element['link']['@href']
                    self.report.append(url)
                    self.is_report = True
                    report_ids.add(_id)
                elif title == '震源・震度に関する情報' and _id not in infomation_ids:
                    url = element['link']['@href']
                    self.infomation.append(url)
                    self.is_infomation = True
                    infomation_ids.add(_id)

                if title in {'震度速報', '震源・震度に関する情報'}:
                    delete_ids.add(_id)

            if self.report != []:
                self.report.reverse()
            if self.infomation != []:
                self.infomation.reverse()

            delete_report = report_ids - delete_ids
            delete_infomation = infomation_ids - delete_ids

            for delete in delete_report:
                report_ids.discard(delete)
            for delete in delete_infomation:
                infomation_ids.discard(delete)

            cache_element = {
                'latest': last_modified,
                'report': list(report_ids),
                'infomation': list(infomation_ids)
            }
            self.__save_cache(cache_element)

    def __load_cache(self, empty_element: Any) -> Any:
        '''
        Load cache file.
        If it does not exist, the argument is returned directly.

        Args:
            empty_element (Any): Element that is returned directly if it does not exist.

        Returns:
            Any: The contents of the cache file. If not present, argument element.
        '''
        if os.path.isfile(self.save_file_path):
            buffer = json_read(self.save_file_path)
        else:
            buffer = empty_element

        return buffer

    def __save_cache(self, element: Any) -> None:
        '''
        Save cache file.

        Args:
            element (Any): The element to store in the cache file.
        '''
        json_write(self.save_file_path, element)
