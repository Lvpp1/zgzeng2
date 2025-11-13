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
temp_path = os.path.join(parent_path, 'temp')
data_path = os.path.join(parent_path, 'data\\VulDetail')



init_url = "https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id=1&keywords=&online_status=0&%24deviceRange=unfix&modulename=device-vul"
VulDeviceNumber = None
result = []


@outerFunction
def init_number(headers):
    """获取未处理风险总共有多少台终端"""
    global VulDeviceNumber
    response = requests.get(init_url, headers=headers, verify=False)
    total = json.loads(response.content.decode())['pagination']['total']
    VulDeviceNumber = total
    logger.info(f'GET {init_url} {response.status_code} CURRENT VIRUDEVICENUMBER {VulDeviceNumber}')

def get_full_data(VulDeviceNumber):
    """获取全量数据"""
    try:
        if isinstance(VulDeviceNumber / 5000, int):
            pages = VulDeviceNumber / 5000 + 1
        elif isinstance(VulDeviceNumber / 5000, float):
            pages = int(VulDeviceNumber / 5000) + 2
        return pages
    except Exception as e:
        logger.error(f"ERROR - {e}")


def get_viru_detail(pages):
    global result
    with open(temp_path, 'r') as fh:
        headers = json.load(fh)
    for page in range(1, pages):
        url = f"https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id=1&keywords=&online_status=0&%24deviceRange=unfix&modulename=device-vul&currentPage={page}&pageSize=5000"
        res = requests.get(url, headers=headers, verify=False)
        response = json.loads(res.text)
        result.extend(response['list'])
        logger.info(f'GET {url} {res.status_code}')


def run():
    init_number()
    pages = get_full_data(VulDeviceNumber)
    get_viru_detail(pages)
    try:
        df = pd.DataFrame(result)
        file_name = "{}.csv".format(datetime.datetime.now().strftime("未修复漏洞涉及设备_%Y_%m_%d_%H_%M_%S"))
        csv_file_path = os.path.join(data_path, file_name)
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        logger.info(f"SUCCESS OUTPUT {csv_file_path}")
    except Exception as e:
        logger.error(f"ERROR - {e}")

if __name__ == '__main__':
    run()
