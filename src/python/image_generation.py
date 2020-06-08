'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import Dict, List

import chromedriver_binary  # noqa: F401 # pylint: disable=W0611
from selenium import webdriver

# Too many arguments is specifications
# pylint: disable=R0913


def create_image(
        save_file_path: str, title: str, areas: Dict[str, List[str]], explanation: List[str],
        max_seismic_intensity: str, epicenter: str, magnitude: str) -> None:
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
        TypeError: The seismic intensity is incorrect.
    '''
    print('create template')
    if not os.path.isdir(os.path.dirname(save_file_path)):
        raise FileNotFoundError('No directory found to save.')
    if len(explanation) < 2:
        raise TypeError('At least two description elements are required.')

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
    elif max_seismic_intensity not in {
            '1', '2', '3', '4', '5弱', '5強', '6弱', '6強', '7', '１', '２', '３', '４', '５弱', '５強', '６弱', '６強', '７'}:
        raise TypeError('The seismic intensity is incorrect.')

    url = f'http://localhost:5000/template?ti={title}&areas={areas}\
&exp={explanation}&max_si={max_seismic_intensity}&epi={epicenter}&mag={magnitude}'

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
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    page_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(1024, page_height)
    driver.execute_script("document.body.style.zoom='100%'")
    driver.save_screenshot(save_file_path)
    driver.quit()
