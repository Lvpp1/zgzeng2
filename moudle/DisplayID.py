import pathlib
import logging
import os
import json


logger = logging.getLogger('my_logger')
parent_path = pathlib.Path(__file__).parent.parent
unitinfo_path = os.path.join(parent_path, 'UnitInfo.txt')


def show_secondary_unit_id():
    with open(unitinfo_path, 'r', encoding='utf8') as file:
        json_data = json.load(file)
    return json_data


def run():
    print("""
    提示：获取的ID格式是ID:单位名称
    比如：229017: 单位名称
    229017是集团二级单位的单位ID号
    """)

    new_data = []
    idlist = show_secondary_unit_id()
    for item in idlist:
        new_data.append({"id": item['id'], "name": item['name']})
    columns_per_line = 4
    max_column_width = 30
    for i in range(0, len(new_data), columns_per_line):
        line = ""
        for j in range(columns_per_line):
            index = i + j
            if index < len(new_data):
                item = f"{new_data[index]['id']}: {new_data[index]['name']}"
                line += item.ljust(max_column_width)
            else:
                line += " " * max_column_width
        print(line.rstrip())

if __name__ == '__main__':
    run()
