'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import multiprocessing
import os
from typing import Any

try:
    from json_operation import json_write, json_read
    from transmission import line, slack, discode
    from push_platform import platform_type_0, platform_type_1, platform_type_2
except ModuleNotFoundError:
    from src.json_operation import json_write, json_read
    from src.transmission import line, slack, discode
    from src.push_platform import platform_type_0, platform_type_1, platform_type_2


class Filter():
    '''
    Filter the information to be sent according to user settings.
    '''

    def __init__(self, user_file_path: str, cache_dir_path: str):
        '''
        Compare the user config with the buffer and send the changes and newly added elements to the configured SNS.

        Args:
            uer_file_path(str): User config json file path.
            cache_dir_path(str): The directory path to save the buffer.
        '''
        self.user_file_path = user_file_path
        self.cache_dir_path = cache_dir_path
        self.cache_file_path = os.path.join(self.cache_dir_path, 'buffre_user_setting.json')

        if os.path.isfile(self.cache_file_path):
            self.users = json_read(self.cache_file_path)
        else:
            self.users = {}

        self.setup()

    def setup(self) -> None:
        '''
        Set up the user config.
        Any new additions or changes will be sent to your platform.
        '''
        # Too many branches is specifications
        # pylint: disable=R0912
        new_users = json_read(self.user_file_path)

        delete_element = set()
        for user_name in self.users:
            if user_name not in new_users:
                delete_element.add(user_name)

        for key in delete_element:
            del self.users[key]

        for user_name in new_users:

            if user_name not in self.users:
                # new accounts
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']

                if new_users[user_name]['areas'] == []:
                    areas = 'All'
                else:
                    areas = '、'.join(new_users[user_name]['areas'])

                seismic_intensity = new_users[user_name]['seismic_intensity']
                if seismic_intensity == '0':
                    seismic_intensity = 'All'

                is_quick_report = new_users[user_name]['is_quick_report']

                text = f'[設定を追加しました]\n- 送信する最低震度: {seismic_intensity}\n- 送信する地域: {areas}\n- 緊急速報の送信: {is_quick_report}'

            elif new_users[user_name]['seismic_intensity'] != self.users[user_name]['seismic_intensity']:
                # changed seismic intensity
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                seismic_intensity = new_users[user_name]['seismic_intensity']
                if seismic_intensity == '0':
                    seismic_intensity = 'All'
                text = f'[設定を変更しました]\n- 送信する最低震度: {seismic_intensity}'

            elif new_users[user_name]['areas'] != self.users[user_name]['areas']:
                # changed areas
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                if new_users[user_name]['areas'] == []:
                    areas = 'All'
                else:
                    areas = '、'.join(new_users[user_name]['areas'])
                text = f'[設定を変更しました]\n- 送信する地域: {areas}'

            elif new_users[user_name]['is_quick_report'] != self.users[user_name]['is_quick_report']:
                # changed quick report
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                is_quick_report = new_users[user_name]['is_quick_report']
                text = f'[設定を変更しました]\n- 緊急速報の送信: {is_quick_report}'

            else:
                continue

            platform = int(new_users[user_name]['platform'])
            if platform == 1:
                line(token, text, None)
            elif platform == 2:
                channel = new_users[user_name]['channel']
                slack(token, channel, text, None)
            elif platform == 3:
                discode(token, text, None)

        json_write(self.cache_file_path, self.users)

    def post_type_0(self, earthquakes: Any) -> None:
        '''
        Filter only text and send to the platform set in the user config.

        Args:
            earthquakes: Earthquake data to send.
        '''
        jobs = []
        for element in earthquakes:
            for user in self.users:
                if self.is_push(element, self.users[user]) and self.users[user]['is_quick_report']:
                    process = multiprocessing.Process(target=platform_type_0, args=(self.users[user], element))
                    jobs.append(process)
                    process.start()

    def post_type_1(self, earthquakes: Any) -> None:
        '''
        Formatted images and seismic intensity distribution maps are
        sent to the platform set in the user config after filtering.

        Args:
            earthquakes: Earthquake data to send.
        '''
        jobs = []
        for element in earthquakes:
            for user in self.users:
                if self.is_push(element, self.users[user]):
                    process = multiprocessing.Process(target=platform_type_1, args=(self.users[user], element))
                    jobs.append(process)
                    process.start()

    def post_type_2(self, earthquakes: Any) -> None:
        '''
        Formatted images are filtered and sent to the platform set in the user config.

        Args:
            earthquakes: Earthquake data to send.
        '''
        jobs = []
        for element in earthquakes:
            for user in self.users:
                if self.is_push(element, self.users[user]):
                    process = multiprocessing.Process(target=platform_type_2, args=(self.users[user], element))
                    jobs.append(process)
                    process.start()

    @staticmethod
    def is_push(earthquake: Any, user: Any) -> bool:
        '''
        Apply user settings and check whether to send.

        Args:
            earthquake: The data to send.
            user: user config.
        Returns:
            bool: Whether to send.
        '''
        user_si = str(user['seismic_intensity'])
        if user_si in {'1', '2', '3', '4', '5-', '5+', '6-', '6+', '7'}:
            template = ['1', '2', '3', '4', '5-', '5+', '6-', '6+', '7']
            seismic_intensity = earthquake['max_seismic_intensity'] in template[template.index(user_si):]
        else:
            seismic_intensity = True

        area = True
        if user['areas'] != []:
            area = bool(set(earthquake['areas']) & set(user['areas']))
        return area and seismic_intensity
