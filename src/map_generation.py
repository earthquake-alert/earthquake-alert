'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import datetime
import os
import signal
import time
from typing import Any, Dict, List, Union

from selenium import webdriver


def create_map_info(
        areas: Dict[str, Union[Any]],
        title: str, date: str, image_file_path: str) -> None:
    '''
    Call the js script and create a seismic intensity distribution map using node.

    Args:
        areas (Dict[str, Union[Any]]):
            Latitude and longitude of seismic intensity observation point and epicenter.
        title (str): title.
        date (str): Earthquake occurrence time.
        image_file_path (str): The path of the generated image.
    '''
    target_time = datetime.datetime.strptime(str(date), r'%Y%m%d%H%M%S')

    url = f'http://map:8080/?ti={title}&date={target_time.strftime(r"%Y%m%d%H%M%S")}'

    url += f'&epi={areas["epicenter"][0]},{areas["epicenter"][1]}'

    for si in areas['areas']:
        positions = set()
        for position in areas['areas'][si]:
            positions.add(f'{position[0]}:{position[1]}')
        url += f'&point{si}={",".join(positions)}'

    captcha(url, image_file_path)


def create_map_repo(areas: Dict[str, List[str]], title: str, date: str, image_file_path: str) -> None:
    '''
    Generates seismic intensity distribution map for seismic intensity flash report.

    Args:
        areas (Dict[str, List[str]]): Subdivision area code according to seismic intensity.
        title (str): title
        date (str): date
        image_file_path (str): The path of the generated image.
    '''
    target_time = datetime.datetime.strptime(str(date), r'%Y%m%d%H%M%S')

    url = f'http://map:8080/?ti={title}&date={target_time.strftime(r"%Y%m%d%H%M%S")}'

    for si in areas:
        positions = set()
        for position in areas[si]:
            positions.add(position)
        url += f'&areas{si}={",".join(positions)}'

    captcha(url, image_file_path)


def captcha(url: str, save_file_path: str) -> None:
    '''
    Use selenium to capture the screen.

    Args:
        url (str): URL to capture.
        save_file_path (str): File path to save the captured image.
    '''
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)

        driver.set_window_size(1920, 1080)
        driver.execute_script("document.body.style.zoom='100%'")
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot(save_file_path)
        driver.quit()
    finally:
        os.kill(driver.service.process.pid, signal.SIGTERM)
