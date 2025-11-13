#! /usr/bin/env python
# --*--coding: utf8



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
data_path = os.path.join(parent_path, 'data')


class FullDate:
    """获取御点用户全量数据"""

    def __init__(self):
        self.device_url = "https://10.201.20.10/api/svr/info?"
        self.device_num = None
        self.full_data = []

    @outerFunction
    def get_device_num(self, headers):
        res = requests.get(self.device_url, headers=headers, verify=False)
        stats_res = res.content.decode()
        stats_data = json.loads(stats_res)
        self.device_num = stats_data['data']['pcTotal']
        logger.info(f'GET {self.device_url} {res.status_code} current users number {self.device_num}')


    def get_data(self, page, headers):
        """singele 请求发送"""
        try:
            url = f"https://10.201.20.10/api/device/show?sorter=id%3Adescend&modulename=device-info&online_status=0&currentPage={page}&pageSize=5000&group_id=1"
            res = requests.get(url, headers=headers, verify=False)
            response = json.loads(res.text)
            self.full_data.extend(response['list'])
            logger.info(f"GET {url} {res.status_code}")
        except Exception as e:
            logger.error(f"ERROR - {e}")

    def get_full_data(self):
        """获取全量数据"""
        try:
            if isinstance(self.device_num / 5000, int):
                pages = self.device_num / 5000 + 1
            elif isinstance(self.device_num / 5000, float):
                pages = int(self.device_num / 5000) + 2
            return pages
        except Exception as e:
            logger.error(f"ERROR - {e}")

    def run(self):
        """输出数据"""
        self.get_device_num()
        with open(temp_path, 'r') as fh:
            headers = json.load(fh)
        pages = self.get_full_data()
        try:
            for page in range(1, pages):
                self.get_data(page, headers)
            df = pd.DataFrame(self.full_data)
            InstallDetail_path = os.path.join(data_path, 'FullDate')
            file_name = "{}.csv".format(datetime.datetime.now().strftime("御点全量数据_%Y_%m_%d_%H_%M_%S"))
            csv_file_path = os.path.join(InstallDetail_path, file_name)
            df.to_csv(csv_file_path, index=False, encoding='utf-8')
            logger.info(f"SUCCESS OUTPUT {csv_file_path}")
        except Exception as e:
            logger.error(f"ERROR - {e}")