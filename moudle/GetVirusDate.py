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
data_path = os.path.join(parent_path, 'data\\VirusDetail')


init_url = "https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id=1&keywords=&online_status=0&%24virusRange=unfix&modulename=device-virus&currentPage=1"
ViruDeviceNumber = None
result = []


@outerFunction
def init_number(headers):
    """获取未处理风险总共有多少台终端"""
    global ViruDeviceNumber
    response = requests.get(init_url, headers=headers, verify=False)
    total = json.loads(response.content.decode())['pagination']['total']
    ViruDeviceNumber = total
    logger.info(f'GET {init_url} {response.status_code} CURRENT VIRUDEVICENUMBER {ViruDeviceNumber}')


def get_full_data(ViruDeviceNumber):
    """获取全量数据"""
    try:
        if isinstance(ViruDeviceNumber / 5000, int):
            pages = ViruDeviceNumber / 5000 + 1
        elif isinstance(ViruDeviceNumber / 5000, float):
            pages = int(ViruDeviceNumber / 5000) + 2
        return pages
    except Exception as e:
        logger.error(f"ERROR - {e}")


def get_viru_detail(pages):
    global result
    with open(temp_path, 'r') as fh:
        headers = json.load(fh)
    for page in range(1, pages):
        url = f"https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id=1&keywords=&online_status=0&%24virusRange=unfix&modulename=device-virus&currentPage={page}&pageSize=5000"
        res = requests.get(url, headers=headers, verify=False)
        response = json.loads(res.text)
        result.extend(response['list'])
        logger.info(f'GET {url} {res.status_code}')


def run():
    init_number()
    pages = get_full_data(ViruDeviceNumber)
    get_viru_detail(pages)
    try:
        df = pd.DataFrame(result)
        file_name = "{}.csv".format(datetime.datetime.now().strftime("未处理风险涉及设备_%Y_%m_%d_%H_%M_%S"))
        csv_file_path = os.path.join(data_path, file_name)
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        logger.info(f"SUCCESS OUTPUT {csv_file_path}")
    except Exception as e:
        logger.error(f"ERROR - {e}")


