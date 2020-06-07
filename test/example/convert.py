'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import json
import re

import xmltodict


def main():
    '''
    convert xml to json.
    '''

    json_fp = 'test/example/2.json'
    xml_fp = '/Users/yuto_w/Downloads/jmaxml_20200525_Samples/32-39_11_05_120615_VXSE53.xml'

    with open(xml_fp) as f:
        text_list = f.readlines()

    text = '\n'.join(text_list)

    xml_root = xmltodict.parse(text)
    explanation = []

    title = xml_root['Report']['Control']['Title']
    explanation.append(xml_root['Report']['Head']['Headline']['Text'])
    explanation += xml_root['Report']['Body']['Comments']['ForecastComment']['Text'].split('\n\n')

    max_seismic_intensity = str(xml_root['Report']['Body']['Intensity']['Observation']['MaxInt'])
    magnitude = xml_root['Report']['Body']['Earthquake']['jmx_eb:Magnitude']['#text']

    location = xml_root['Report']['Body']['Earthquake']['Hypocenter']['Area']['jmx_eb:Coordinate']['#text']

    _location = re.findall(r'\+(?P<lon>.+)\+(?P<lat>.+)\-.+', location)

    epicenter = {
        'name': xml_root['Report']['Body']['Earthquake']['Hypocenter']['Area']['Name'],
        'lon': float(_location[0][0]),
        'lat': float(_location[0][1])
    }

    si_7 = set()
    si_over_6 = set()
    si_under_6 = set()
    si_over_5 = set()
    si_under_5 = set()
    si_4 = set()
    si_3 = set()
    si_2 = set()
    si_1 = set()

    def pref(_areas):
        def area(_city):
            def city(_areas_2):
                def intensity_station(_areas_3):
                    sint = _areas_3['Int']

                    if sint == '7':
                        si_7.add(_areas_3['Code'])
                    elif sint == '6+':
                        si_over_6.add(_areas_3['Code'])
                    elif sint == '6-':
                        si_under_6.add(_areas_3['Code'])
                    elif sint == '5+':
                        si_over_5.add(_areas_3['Code'])
                    elif sint == '5-':
                        si_under_5.add(_areas_3['Code'])
                    elif sint == '4':
                        si_4.add(_areas_3['Code'])
                    elif sint == '3':
                        si_3.add(_areas_3['Code'])
                    elif sint == '2':
                        si_2.add(_areas_3['Code'])
                    elif sint == '1':
                        si_1.add(_areas_3['Code'])

                if isinstance(_areas_2['IntensityStation'], list):
                    for element in _areas_2['IntensityStation']:
                        intensity_station(element)
                else:
                    intensity_station(_areas_2['IntensityStation'])

            if isinstance(_city['City'], list):
                for element in _city['City']:
                    city(element)
            else:
                city(_city['City'])

        if isinstance(_areas['Area'], list):
            for element in _areas['Area']:
                area(element)
        else:
            area(_areas['Area'])

    # エリアの整形
    areas = xml_root['Report']['Body']['Intensity']['Observation']['Pref']
    if isinstance(areas, list):
        for element in areas:
            pref(element)
    else:
        pref(areas)

    areas = {
        '7': list(si_7),
        '6+': list(si_over_6),
        '6-': list(si_under_6),
        '5+': list(si_over_5),
        '5-': list(si_under_5),
        '4': list(si_4),
        '3': list(si_3),
        '2': list(si_2),
        '1': list(si_1)
    }

    output = {
        'title': title,
        'max_seismic_intensity': max_seismic_intensity,
        'magnitude': magnitude,
        'explanation': explanation,
        'epicenter': epicenter,
        'areas': areas
    }

    with open(json_fp, mode='w') as contents:
        json.dump([output], contents, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
