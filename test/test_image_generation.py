'''
@author: Yuto Watanabe

Copyright (c) 2020 Earthquake alert
'''
import os

import pytest
from src.python.image_generation import create_image

DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_images')
if not os.path.isdir(DIRECTORY):
    os.makedirs(DIRECTORY)


@pytest.mark.parametrize(
    'title, areas, fp_name', [
        ('テストタイトル', {'ここに震度': ['いばらぎ']}, 1),
        ('テストタイトル', {'震度５強': ['hoge', 'foo', 'nya'], '震度５弱': ['haha', 'hyu-', 'wan'], '震度４': ['apple', 'orange']}, 2),
        ('', {'': []}, 3),
        ('abcd', {'efgh': ['hijk']}, 4),
        ('テストタイトル', {'': ['hoge', 'hoge']}, 5),
        ('テストタイトル', {'1': [], '2': [], '3': []}, 6),
    ]
)
def test_create_image_title_area(title, areas, fp_name):
    '''
    画像生成テスト。
    タイトルとエリアを変更し、テストを実行します。
    '''
    explanation = ['解説1', '解説2']
    max_seismic_intensity = '３'
    epicenter = '太平洋沖'
    magnitude = 5.7
    assert create_image(os.path.join(DIRECTORY, f'{fp_name}.png'), title, areas,
                        explanation, max_seismic_intensity, epicenter, magnitude) is None


@pytest.mark.parametrize(
    'explanation, max_seismic_intensity, fp_name', [
        (['', ''], '', 7),
        (['hoge', 'foo'], '+5', 8),
        (['hoge', 'foo'], '6弱', 9)
    ]
)
def test_create_image_explanation_max_seismic_intensity(explanation, max_seismic_intensity, fp_name):
    '''
    画像生成テスト。
    タイトルとエリアを変更し、テストを実行します。
    '''
    title = 'テストタイトル'
    areas = {'ここに震度': ['いばらぎ']}
    epicenter = '太平洋沖'
    magnitude = 5.7
    assert create_image(os.path.join(DIRECTORY, f'{fp_name}.png'), title, areas,
                        explanation, max_seismic_intensity, epicenter, magnitude) is None


@pytest.mark.parametrize(
    'epicenter, magnitude, fp_name', [
        ('', 0.0, 10),
        ('abcde', 30.5, 11)
    ]
)
def test_create_image_epicenter_magnitude(epicenter, magnitude, fp_name):
    '''
    画像生成テスト。
    タイトルとエリアを変更し、テストを実行します。
    '''
    title = 'テストタイトル'
    areas = {'ここに震度': ['いばらぎ']}
    explanation = ['解説1', '解説2']
    max_seismic_intensity = '３'
    assert create_image(os.path.join(DIRECTORY, f'{fp_name}.png'), title, areas,
                        explanation, max_seismic_intensity, epicenter, magnitude) is None


@pytest.mark.parametrize(
    'change, element, expectation', [
        ('explanation', ['hoge'], pytest.raises(TypeError)),
        ('magnitude', '3', pytest.raises(TypeError)),
        ('max_seismic_intensity', 5, pytest.raises(TypeError))
    ]
)
def test_create_image_raise(expectation, change, element):
    title = 'テストタイトル'
    areas = {'ここに震度': ['いばらぎ']}
    explanation = ['解説1', '解説2']
    max_seismic_intensity = '３'
    epicenter = '太平洋沖'
    magnitude = 5.7

    if change == 'title':
        title = element
    elif change == 'areas':
        areas = element
    elif change == 'explanation':
        explanation = element
    elif change == 'max_seismic_intensity':
        max_seismic_intensity = element
    elif change == 'epicenter':
        epicenter = element
    elif change == 'magnitude':
        magnitude = element

    with expectation:
        create_image(os.path.join(DIRECTORY, 'raises.png'), title, areas,
                     explanation, max_seismic_intensity, epicenter, magnitude)
