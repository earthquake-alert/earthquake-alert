'''
@author: Yuto Watanabe

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import Dict, List

# Too many arguments is specifications
# pylint: disable=R0913


def create_image(
        save_file_path: str, title: str, areas: Dict[str, List[str]], explanation: List[str],
        max_seismic_intensity: str, epicenter: str, magnitude: float) -> None:
    '''
    Create a image using `pillow`.

    Args:
        save_file_path (str): The path of the image to save.
        title (str): title.
        areas (Dict[str, List[str]]): Observation area.
        explanation (List[str]): Commentary. (2 elements)
        max_seismic_intensity (str): Maximum seismic intensity.
        epicenter (str): Epicenter.
        magnitude (float): Magnitude.

    Raises:
        FileNotFoundError: No directory found to save.
        TypeError: There are two elements in the list of argument `explanation`.
        TypeError: magnitude should be float.
        TypeError: The seismic intensity is incorrect.
    '''
    if not os.path.isdir(os.path.dirname(save_file_path)):
        raise FileNotFoundError('No directory found to save.')
    if len(explanation) != 2:
        raise TypeError('There are two elements in the list of argument `explanation`.')
    if not isinstance(magnitude, float):
        raise TypeError('magnitude should be float.')

    if title == '':
        title = 'No data.'
    if epicenter == '':
        epicenter = 'No data.'

    if max_seismic_intensity == '':
        max_seismic_intensity = 'No data.'
    elif max_seismic_intensity in ('-5', '5-', '−５', '５−'):
        max_seismic_intensity = '5弱'
    elif max_seismic_intensity in ('+5', '5+', '＋５', '５＋'):
        max_seismic_intensity = '5強'
    elif max_seismic_intensity in ('-6', '6-', 'ー６', '６ー'):
        max_seismic_intensity = '6弱'
    elif max_seismic_intensity in ('+6', '6+', '６＋', '＋６'):
        max_seismic_intensity = '6強'
    elif max_seismic_intensity not in ('1', '2', '3', '4', '5弱', '5強', '6弱', '6強' '7', '１',
                                       '２', '３', '４', '５弱', '５強', '６弱', '６強' '７'):
        raise TypeError('The seismic intensity is incorrect.')
