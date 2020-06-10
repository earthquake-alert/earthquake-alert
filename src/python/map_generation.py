'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import os
import subprocess  # skipcq: BAN-B404
from typing import Any

try:
    from json_operation import json_write
except ModuleNotFoundError:
    from src.python.json_operation import json_write


def create_map(areas: Any, image_file_path: str):
    '''
    Call the js script and create a seismic intensity distribution map using node.

    Args:
        areas (Any): Data used for seismic intensity map.
        image_file_path (str): The path of the generated image.
    '''
    print('create map')
    run_file_path = os.path.join('src', 'external', 'map-draw', 'src', 'mapping.js')
    convert_file_path = os.path.join('src', 'external', 'map-draw', 'src', 'convert.js')
    config_file_path = os.path.join('config', 'map_draw.json')

    cache_dir = os.path.dirname(image_file_path)
    svg_file_path = os.path.join(cache_dir, 'map.svg')
    json_file_path = os.path.join(cache_dir, 'mapping.json')

    json_write(json_file_path, areas)

    run_command = ['node', run_file_path, '-i', json_file_path, '-o', svg_file_path, '-c', config_file_path]
    convert_command = ['node', convert_file_path, '-i', svg_file_path, '-o', image_file_path]

    subprocess.run(run_command, check=True)      # skipcq: BAN-B603
    subprocess.run(convert_command, check=True)  # skipcq: BAN-B603

    os.remove(svg_file_path)
