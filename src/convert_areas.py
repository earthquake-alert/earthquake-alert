'''
@author: Yuto Watanabe
@version: 2.0.0

Copyright (c) 2020 Earthquake alert
'''
import datetime
import glob
import multiprocessing
import os
import shutil
import sqlite3
from typing import Any, Dict, List

try:
    from image_generation import create_image, create_image_report  # pyright: reportMissingImports=false
    from map_generation import create_map_info, create_map_repo  # pyright: reportMissingImports=false
except ModuleNotFoundError:
    from src.image_generation import create_image, create_image_report
    from src.map_generation import create_map_info, create_map_repo

# Too many variables is specifications
# pylint: disable=R0914


def convert(earthquakes: List[Dict[str, Any]], db_file_path: str, image_directory_path: str) -> List[Dict[str, Any]]:
    '''
    The JMA seismic intensity area code is divided into two pieces of data,
    area name and latitude/longitude, and the map path is drawn using them,
    the template is applied, and the file path is attached and returned.

    Args:
        earthquakes (List[Dict[str, Any]]): Formatted Json data obtained from the Japan Meteorological Agency.
        db_file_path (str): Region code database file path.
        image_directory_path(str): directory of save image.

    Returns:
        List[Dict[str, Any]]: Data that contains the information to send and the image path.
    '''
    now = datetime.datetime.now()
    converted = []

    image_dir = os.path.join(image_directory_path, now.strftime(r'%Y%m%d%H%M%S'))
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)

    delete_process = multiprocessing.Process(target=delete_directory,
                                             args=(image_directory_path, now))
    delete_process.start()

    conn = sqlite3.connect(db_file_path)
    table = conn.cursor()

    for key, element in enumerate(earthquakes):
        map_file_path = os.path.join(image_dir, f'map_{key}.png')
        template_file_path = os.path.join(image_dir, f'template_{key}.png')

        max_seismic_intensity_locations = [element['epicenter']['lat'], element['epicenter']['lon']]

        converted_areas = {}
        si_location = {}
        prefectures = set()

        for seismic_intensity in element['areas']:
            locations = []
            names = set()
            map_seismic_intensity, template_seismic_intensity = change_seismic_intensity(seismic_intensity)

            for code in element['areas'][seismic_intensity]:
                for colum in table.execute(f"SELECT * FROM areas WHERE code='{code}'"):
                    names.add(colum[6])
                    locations.append([colum[4], colum[5]])
                    prefectures.add(colum[1])

            si_location[map_seismic_intensity] = locations
            if element['max_seismic_intensity'] not in {
                    '1', '2', '3', '１', '２', '３', '震度1', '震度2', '震度3', '震度１', '震度２', '震度３'}:
                if template_seismic_intensity in {'震度3', '震度4', '震度5弱', '震度5強', '震度6弱', '震度6強', '震度7'}:
                    converted_areas[template_seismic_intensity] = list(names)
            else:
                converted_areas[template_seismic_intensity] = list(names)

        converted_location = {
            'epicenter': max_seismic_intensity_locations,
            'areas': si_location
        }
        process = multiprocessing.Process(target=create_image, args=(
            template_file_path,
            element['title'],
            converted_areas,
            element['explanation'],
            element['max_seismic_intensity'],
            element['epicenter']['name'],
            element['magnitude'],
            element['date']
        ))
        process.start()

        if not element['is_cancel']:
            process_2 = multiprocessing.Process(target=create_map_info, args=(
                converted_location,
                element['title'],
                element['date'],
                map_file_path
            ))
            process_2.start()
            process_2.join()
        else:
            map_file_path = ''
        process.join()

        target_time = datetime.datetime.strptime(str(element['date']), r'%Y%m%d%H%M%S')
        text = f"{target_time.strftime(r'%d日%H時%M分')}ころ{element['epicenter']['name']}を震源とする地震がありました。"
        text += f"震源の規模を示すマグニチュードは{element['max_seismic_intensity']}と推定されています。"
        text += element['explanation'][1]

        converted.append({
            'title': element['title'],
            'text': text,
            'max_seismic_intensity': element['max_seismic_intensity'],
            'explanation': element['explanation'],
            'epicenter': element['epicenter']['name'],
            'areas': list(prefectures),
            'template_path': template_file_path,
            'map_path': map_file_path,
            'type': 1
        })

    delete_process.join()

    return converted


def convert_report(
        earthquakes: List[Dict[str, Any]], db_file_path: str, image_directory_path: str) -> List[Dict[str, Any]]:
    '''
    Apply the template. For seismic intensity flash report.

    Args:
        earthquakes (List[Dict[str, Any]]): Formatted Json data obtained from the Japan Meteorological Agency.
        image_directory_path (str): directory of save image.
        db_file_path (str): Region code database file path.

    Returns:
        List[Dict[str, Any]]: Data that contains the information to send and the image path.
    '''
    now = datetime.datetime.now()
    converted = []

    image_dir = os.path.join(image_directory_path, now.strftime(r'%Y%m%d%H%M%S'))
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)

    delete_process = multiprocessing.Process(target=delete_directory,
                                             args=(image_directory_path, now))
    delete_process.start()

    conn = sqlite3.connect(db_file_path)
    table = conn.cursor()

    for key, element in enumerate(earthquakes):
        template_file_path = os.path.join(image_dir, f'template_report_{key}.png')
        map_file_path = os.path.join(image_dir, f'map_{key}.png')
        prefectures = set()

        for areas in element['areas']:
            for area in element['areas'][areas]:
                table.execute(f"SELECT * FROM pref WHERE city='{area}'")
                prefectures.add(table.fetchall()[0][0])

        process = multiprocessing.Process(target=create_image_report, args=(
            template_file_path,
            element['title'],
            element['areas'],
            element['explanation'],
            element['max_seismic_intensity'],
            element['date']
        ))
        process.start()

        process2 = multiprocessing.Process(target=create_map_repo, args=(
            element['codes'],
            element['title'],
            element['date'],
            map_file_path,
        ))
        process2.start()

        process.join()
        process2.join()

        target_time = datetime.datetime.strptime(str(element['date']), r'%Y%m%d%H%M%S')
        text = f"{target_time.strftime(r'%d日%H時%M分')}ころ地震がありました。"
        text += f"最大震度{change_seismic_intensity(element['max_seismic_intensity'])[1]}を観測しています。"
        text += element['explanation'][1]

        converted.append({
            'title': element['title'],
            'text': text,
            'max_seismic_intensity': element['max_seismic_intensity'],
            'explanation': element['explanation'],
            'areas': list(prefectures),
            'template_path': template_file_path,
            'map_path': map_file_path,
            'type': 1
        })

    delete_process.join()

    return converted


def delete_directory(directory: str, now: datetime.datetime) -> None:
    '''
    Delete the directories you added more than a day ago.

    Args:
        directory (str): The directory to be deleted.
        now (datetime.datetime): The current time.
    '''
    date_directory = glob.glob(os.path.join(directory, '**' + os.sep), recursive=True)
    delete_image_directory = set()

    for element in date_directory:
        try:
            date = datetime.datetime.strptime(os.path.basename(element.rstrip(os.sep)), r'%Y%m%d%H%M%S')
            diff_date = now - date
            if diff_date.days > 1:
                delete_image_directory.add(element)
        except ValueError:
            pass

    for element in delete_image_directory:
        shutil.rmtree(element)


def change_seismic_intensity(seismic_intensity: str) -> tuple:
    '''
    Converts the seismic intensity display into a format for map display.

    Args:
        seismic_intensity (str): Default seismic intensity display

    Returns:
        tuple: Display converted for map.
    '''
    formated_seismic_ontensity = ('0', '震度0')
    if seismic_intensity in {'1', '１', '震度1', '震度１'}:
        formated_seismic_ontensity = ('1', '震度1')
    elif seismic_intensity in {'2', '２', '震度2', '震度２'}:
        formated_seismic_ontensity = ('2', '震度2')
    elif seismic_intensity in {'3', '３', '震度3', '震度３'}:
        formated_seismic_ontensity = ('3', '震度3')
    elif seismic_intensity in {'4', '４', '震度4', '震度４'}:
        formated_seismic_ontensity = ('4', '震度4')
    elif seismic_intensity in {'5-', '-5', '５-', '-５', '震度5弱', '震度５弱'}:
        formated_seismic_ontensity = ('5l', '震度5弱')
    elif seismic_intensity in {'5+', '+5', '５+', '+５', '震度5強', '震度５強'}:
        formated_seismic_ontensity = ('5u', '震度5強')
    elif seismic_intensity in {'6-', '-6', '６-', '-６', '震度6弱', '震度６弱'}:
        formated_seismic_ontensity = ('6l', '震度6弱')
    elif seismic_intensity in {'6+', '+6', '６+', '+６', '震度6強', '震度６強'}:
        formated_seismic_ontensity = ('6u', '震度6強')
    elif seismic_intensity in {'7', '７', '震度7', '震度７'}:
        formated_seismic_ontensity = ('7', '震度7')

    return formated_seismic_ontensity
