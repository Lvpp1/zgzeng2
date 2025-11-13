
import json
import requests
from common.temp import outerFunction
import logging
import pathlib
import os
import pandas as pd
import datetime



requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')
parent_path = pathlib.Path(__file__).parent.parent
company_path = os.path.join(parent_path, 'company')
corepath = os.path.join(parent_path, "data\\Core")


urllist = ["https://10.201.20.10/api/report/getMarkList?sorter=device_mark%3Adescend&groupId=1&tableId=secoverview%2Fgroup&currentPage=1&pageSize=100",
    "https://10.201.20.10/api/report/getMarkList?sorter=device_mark%3Adescend&groupId=302955&tableId=secoverview%2Fgroup&currentPage=1&pageSize=100",
    "https://10.201.20.10/api/report/getMarkList?sorter=device_mark%3Adescend&groupId=238688&tableId=secoverview%2Fgroup&currentPage=1&pageSize=100",
    "https://10.201.20.10/api/report/getMarkList?sorter=device_mark%3Adescend&groupId=242753&tableId=secoverview%2Fgroup&currentPage=1&pageSize=100"]

result = []
def get_unit():
    """获取所有单位名称,存放在列表中"""
    unit_list = []
    try:
        with open(company_path, 'r', encoding='utf8') as fh:
            contents = fh.readlines()
        for item in contents:
            if '-' in item:
                unit_list.append(item.split('-')[1].replace('\n', ''))
            elif '\n' in item:
                unit_list.append(item.replace('\n', ''))
            else:
                unit_list.append(item)
        logger.info(f"GET COMPANY SUCCESS")
        return unit_list
    except Exception as e:
        logger.error(f'ERROR - {e}')

@outerFunction
def get_core(headers):
    """获取评分情况"""
    global result
    for url in urllist:
        res = requests.get(url, headers=headers, verify=False)
        response = res.content.decode()
        data = json.loads(response)
        result.extend(data['list'])
        logger.info(f'GET {url} {res.status_code}')


def run():
    """获取与输出数据"""
    get_core()
    unit_list = get_unit()
    try:
        res = [{'单位名称': item['name'], "评分": item['overall_mark']} for item in result if item['name'] in unit_list]
        df = pd.DataFrame(res)
        file_name = "{}.csv".format(datetime.datetime.now().strftime("评分_%Y_%m_%d_%H_%M_%S"))
        csv_file_path = os.path.join(corepath, file_name)
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        logger.info(f"SUCCESS WRITE INTO {csv_file_path}")
    except Exception as e:
        logger.error(f"ERROR - {e}")


if __name__ == '__main__':
    run()





