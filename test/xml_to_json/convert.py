import json

import xmltodict


def main():
    path = 'test/xml_to_json/test5.xml'
    with open(path) as f:
        text_list = f.readlines()

    text = '\n'.join(text_list)

    output = xmltodict.parse(text)

    with open('test/xml_to_json/output.json', mode='w') as contents:
        json.dump([output], contents, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
