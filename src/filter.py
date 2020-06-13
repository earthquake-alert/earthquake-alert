'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import Any

try:
    from json_operation import json_write, json_read
    from transmission import line, slack, discode
except ModuleNotFoundError:
    from src.json_operation import json_write, json_read
    from src.transmission import line, slack, discode


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

        cache_file_path = os.path.join(cache_dir_path, 'buffre_user_setting.json')
        if os.path.isfile(cache_file_path):
            self.users = json_read(cache_file_path)
        else:
            self.users = {}

        new_users = json_read(user_file_path)

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

                text = f'[設定を追加しました]\n送信する最低震度: {seismic_intensity}\n送信する地域: {areas}\n緊急速報の送信: {is_quick_report}'

            elif new_users[user_name]['seismic_intensity'] != self.users[user_name]['seismic_intensity']:
                # changed seismic intensity
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                seismic_intensity = new_users[user_name]['seismic_intensity']
                if seismic_intensity == '0':
                    seismic_intensity = 'All'
                text = f'[設定を変更しました]\n送信する最低震度: {seismic_intensity}'

            elif new_users[user_name]['areas'] != self.users[user_name]['areas']:
                # changed areas
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                if new_users[user_name]['areas'] == []:
                    areas = 'All'
                else:
                    areas = '、'.join(new_users[user_name]['areas'])
                text = f'[設定を変更しました]\n送信する地域: {areas}'

            elif new_users[user_name]['is_quick_report'] != self.users[user_name]['is_quick_report']:
                # changed quick report
                self.users[user_name] = new_users[user_name]

                token = new_users[user_name]['token']
                is_quick_report = new_users[user_name]['is_quick_report']
                text = f'[設定を変更しました]\n緊急速報の送信: {is_quick_report}'

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

        json_write(cache_file_path, self.users)

    def post_type_0(self, earthquakes: Any):
        '''
        Filter only text and send to the platform set in the user config.

        Args:
            earthquakes: Earthquake data to send.
        '''
        for element in earthquakes:
            for user in self.users:
                if self.is_check(element, self.users[user]):
                    token = self.users[user]['token']
                    text = element['text']
                    platform = int(self.users[user]['platform'])
                    if platform == 1:
                        line(token, text, None)
                    elif platform == 2:
                        channel = self.users[user]['channel']
                        slack(token, channel, text, None)
                    elif platform == 3:
                        discode(token, text, None)

    def post_type_1(self, earthquakes: Any):
        '''
        Formatted images and seismic intensity distribution maps are
        sent to the platform set in the user config after filtering.

        Args:
            earthquakes: Earthquake data to send.
        '''
        for element in earthquakes:
            for user in self.users:
                if self.is_check(element, self.users[user]):
                    token = self.users[user]['token']
                    template_path = element['template_path']
                    map_path = element['map_path']
                    platform = int(self.users[user]['platform'])
                    if platform == 1:
                        line(token, '地震情報', template_path)
                        line(token, '震度分布図', map_path)
                    elif platform == 2:
                        channel = self.users[user]['channel']
                        slack(token, channel, '地震情報', template_path)
                        slack(token, channel, '震度分布図', map_path)
                    elif platform == 3:
                        discode(token, '地震情報', template_path)
                        discode(token, '震度分布図', map_path)

    def post_type_２(self, earthquakes: Any):
        '''
        Formatted images are filtered and sent to the platform set in the user config.

        Args:
            earthquakes: Earthquake data to send.
        '''
        for element in earthquakes:
            for user in self.users:
                if self.is_check(element, self.users[user]):
                    token = self.users[user]['token']
                    template_path = element['template_path']
                    platform = int(self.users[user]['platform'])
                    if platform == 1:
                        line(token, '地震情報', template_path)
                    elif platform == 2:
                        channel = self.users[user]['channel']
                        slack(token, channel, '地震情報', template_path)
                    elif platform == 3:
                        discode(token, '地震情報', template_path)

    @staticmethod
    def is_check(earthquake: Any, user: Any) -> bool:
        '''
        Apply user settings and check whether to send.

        Args:
            earthquake: The data to send.
            user: user config.
        Returns:
            bool: Whether to send.
        '''
        if user['seismic_intensity'] == '1':
            seismic_intensity = user['max_seismic_intensity'] in '1'
        elif user['seismic_intensity'] == '2':
            seismic_intensity = user['max_seismic_intensity'] in {'1', '2'}
        elif user['seismic_intensity'] == '3':
            seismic_intensity = user['max_seismic_intensity'] in {'1', '2', '3'}
        elif user['seismic_intensity'] == '4':
            seismic_intensity = user['max_seismic_intensity'] in {'1', '2', '3', '4'}
        elif user['seismic_intensity'] in {'5-', '-5', '5弱'}:
            seismic_intensity = user['max_seismic_intensity'] not in {
                '5-', '-5', '5弱', '5+', '+5', '5強', '6-', '-6', '6弱', '6+', '+6', '6強', '7'}
        elif user['seismic_intensity'] in {'5+', '+5', '5強'}:
            seismic_intensity = user['max_seismic_intensity'] not in {
                '5+', '+5', '5強', '6-', '-6', '6弱', '6+', '+6', '6強', '7'}
        elif user['seismic_intensity'] in {'6-', '-6', '6弱'}:
            seismic_intensity = user['max_seismic_intensity'] not in {'6-', '-6', '6弱', '6+', '+6', '6強', '7'}
        elif user['seismic_intensity'] in {'6+', '+6', '6強'}:
            seismic_intensity = user['max_seismic_intensity'] not in {'6+', '+6', '6強', '7'}
        elif user['seismic_intensity'] == '7':
            seismic_intensity = user['max_seismic_intensity'] not in {'7'}
        else:
            seismic_intensity = True

        area = bool(set(earthquake['areas']) & set(user['areas']))
        return area and seismic_intensity
