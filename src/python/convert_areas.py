'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import datetime
import os
import sqlite3
from typing import Any, Dict, List

try:
    from image_generation import create_image
    from map_generation import create_map
except ModuleNotFoundError:
    from src.python.image_generation import create_image
    from src.python.map_generation import create_map

# Too many arguments and variables is specifications
# pylint: disable=R0913
# pylint: disable=R0914


def convert(earthquakes: List[Dict[str, Any]], db_file_path: str, image_file_path: str) -> List[Dict[str, Any]]:
    '''
    The JMA seismic intensity area code is divided into two pieces of data,
    area name and latitude/longitude, and the map path is drawn using them,
    the template is applied, and the file path is attached and returned.

    Args:
        earthquakes (List[Dict[str, Any]]): Formatted Json data obtained from the Japan Meteorological Agency.
                                            example: design/sample_data/get_earthquake.json
        db_file_path (str): Region code database file path,
        image_file_path(str): directory of save image.

    Returns:
        List[Dict[str, Any]]: Data that contains the information to send and the image path.
    '''
    now = datetime.datetime.now()
    converted = []

    image_dir = os.path.join(image_file_path, now.strftime(r'%Y%m%d%H%M%S'))
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)

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
            names = []

            for code in element['areas'][seismic_intensity]:
                for colum in table.execute(f"SELECT * FROM areas WHERE code='{code}'"):
                    names.append(colum[2])
                    locations.append([colum[5], colum[4]])
                    prefectures.add(colum[1])

            converted_areas[seismic_intensity] = names
            si_location[change_seismic_intensity(seismic_intensity)] = locations

        converted_location = {
            'epicenter': max_seismic_intensity_locations,
            'areas': si_location
        }

        create_image(
            save_file_path=template_file_path,
            title=element['title'],
            areas=converted_areas,
            explanation=element['explanation'],
            max_seismic_intensity=element['max_seismic_intensity'],
            epicenter=element['epicenter']['name'],
            magnitude=element['magnitude']
        )
        create_map(
            areas=converted_location,
            image_file_path=map_file_path
        )

        converted.append({
            'title': element['title'],
            'max_seismic_intensity': element['max_seismic_intensity'],
            'explanation': element['explanation'],
            'epicenter': element['epicenter']['name'],
            'areas': list(prefectures),
            'template_path': template_file_path,
            'map_path': map_file_path
        })

        print(converted_areas)
        print(converted_location)

    return converted


def change_seismic_intensity(seismic_intensity: str) -> str:
    '''
    Converts the seismic intensity display into a format for map display.

    Args:
        seismic_intensity (str): Default seismic intensity display

    Returns:
        str: Display converted for map.
    '''
    formated_seismic_ontensity = '0'
    if seismic_intensity in ('1', '１', '震度1', '震度１'):
        formated_seismic_ontensity = '1'
    elif seismic_intensity in ('2', '２', '震度2', '震度２'):
        formated_seismic_ontensity = '2'
    elif seismic_intensity in ('3', '３', '震度3', '震度３'):
        formated_seismic_ontensity = '3'
    elif seismic_intensity in ('4', '４', '震度4', '震度４'):
        formated_seismic_ontensity = '4'
    elif seismic_intensity in ('5-', '-5', '５-', '-５', '震度5弱', '震度５弱'):
        formated_seismic_ontensity = '5-'
    elif seismic_intensity in ('5+', '+5', '５+', '+５', '震度5強', '震度５強'):
        formated_seismic_ontensity = '5+'
    elif seismic_intensity in ('6-', '-6', '６-', '-６', '震度6弱', '震度６弱'):
        formated_seismic_ontensity = '6-'
    elif seismic_intensity in ('6+', '+6', '６+', '+６', '震度6強', '震度６強'):
        formated_seismic_ontensity = '6+'
    elif seismic_intensity in ('7', '７', '震度7', '震度７'):
        formated_seismic_ontensity = '7'

    return formated_seismic_ontensity
