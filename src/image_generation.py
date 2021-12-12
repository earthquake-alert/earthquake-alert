'''
@author: Yuto Watanabe
@version: 1.5.0

Copyright (c) 2020 Earthquake alert
'''
import datetime
import os
import signal
import time
from typing import Dict, List

from selenium import webdriver

# Too many arguments is specifications
# pylint: disable=R0913


def create_image(
        save_file_path: str, title: str, areas: Dict[str, List[str]], explanation: List[str],
        max_seismic_intensity: str, epicenter: str, magnitude: str, date: str) -> None:
    '''
    Create a image using `pillow`.

    Args:
        save_file_path (str): The path of the image to save.
        title (str): title.
        areas (Dict[str, List[str]]): Observation area.
        explanation (List[str]): Commentary. (2 or more elements)
        max_seismic_intensity (str): Maximum seismic intensity.
        epicenter (str): Epicenter.
        magnitude (str): Magnitude.

    Raises:
        FileNotFoundError: No directory found to save.
        TypeError: There are two elements in the list of argument `explanation`.
    '''
    if date == '':
        target_time = ''
    else:
        target_time = datetime.datetime.strptime(str(date), r'%Y%m%d%H%M%S').strftime(r"%Y%m%d%H%M%S")

    if not os.path.isdir(os.path.dirname(save_file_path)):
        raise FileNotFoundError('No directory found to save.')

    if ('遠地地震' in title) and (len(explanation) > 4):
        explanation = explanation[:4]

    if title == '':
        title = 'No data.'
    if epicenter == '':
        epicenter = 'No data.'

    if max_seismic_intensity == '':
        max_seismic_intensity = 'No data.'
    elif max_seismic_intensity in {'-5', '5-', '−５', '５−'}:
        max_seismic_intensity = '5弱'
    elif max_seismic_intensity in {'+5', '5+', '＋５', '５＋'}:
        max_seismic_intensity = '5強'
    elif max_seismic_intensity in {'-6', '6-', 'ー６', '６ー'}:
        max_seismic_intensity = '6弱'
    elif max_seismic_intensity in {'+6', '6+', '６＋', '＋６'}:
        max_seismic_intensity = '6強'

    url = f'http://template:5000/template?ti={title}&areas={areas}\
&exp={explanation}&max_si={max_seismic_intensity}&epi={epicenter}\
&mag={magnitude}&date={target_time}'

    captcha(url, save_file_path)


def create_image_report(save_file_path: str, title: str, areas: Dict[str, List[str]], explanation: List[str],
                        max_seismic_intensity: str, date: str) -> None:
    '''
    Create a image using `pillow`.
    For seismic intensity flash report

    Args:
        save_file_path (str): The path of the image to save.
        title (str): title.
        areas (Dict[str, List[str]]): Observation area.
        explanation (List[str]): Commentary. (2 or more elements)
        max_seismic_intensity (str): Maximum seismic intensity.

    Raises:
        FileNotFoundError: No directory found to save.
        TypeError: There are two elements in the list of argument `explanation`.
    '''
    target_time = datetime.datetime.strptime(str(date), r'%Y%m%d%H%M%S')

    if not os.path.isdir(os.path.dirname(save_file_path)):
        raise FileNotFoundError('No directory found to save.')
    if len(explanation) < 2:
        raise TypeError('At least two description elements are required.')

    if title == '':
        title = 'No data.'

    if max_seismic_intensity == '':
        max_seismic_intensity = 'No data.'
    elif max_seismic_intensity in {'-5', '5-', '−５', '５−'}:
        max_seismic_intensity = '5弱'
    elif max_seismic_intensity in {'+5', '5+', '＋５', '５＋'}:
        max_seismic_intensity = '5強'
    elif max_seismic_intensity in {'-6', '6-', 'ー６', '６ー'}:
        max_seismic_intensity = '6弱'
    elif max_seismic_intensity in {'+6', '6+', '６＋', '＋６'}:
        max_seismic_intensity = '6強'

    url = f'http://template:5000/report?ti={title}\
&areas={areas}&exp={explanation}&max_si={max_seismic_intensity}&date={target_time.strftime(r"%Y%m%d%H%M%S")}'

    captcha(url, save_file_path)


def captcha(url: str, save_file_path: str) -> None:
    '''
    Use selenium to capture the screen.

    Args:
        url (str): URL to capture.
        save_file_path (str): File path to save the captured image.
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(0.5)
        page_height = driver.execute_script('return document.body.scrollHeight')
        page_height = min(page_height, 2048)
        driver.set_window_size(1024, page_height)
        time.sleep(0.5)
        driver.execute_script("document.body.style.zoom='100%'")
        driver.save_screenshot(save_file_path)
        driver.quit()
    finally:
        driver.quit()
