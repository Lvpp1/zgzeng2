#! /usr/bin/env python
# --*--coding: utf8

import json
import requests
from common.temp import outerFunction
import logging
import pathlib
import os
from common.unit import get_unit
import pandas as pd
import datetime


requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')
parent_path = pathlib.Path(__file__).parent.parent
UnitInfo_path = os.path.join(parent_path, 'UnitInfo.txt')
temp_path = os.path.join(parent_path, 'temp')
cooperativeunits_path = os.path.join(parent_path, 'CooperativeUnits')
data_path = os.path.join(parent_path, 'data')

parent_id = [1, 238688, 302955, 242753]
urllist = ['https://10.201.20.10/api/group/orgChildGroup?sorter=id%3Aasc&parent_id={}'.format(item) for item in parent_id]

full_data = []
filter_data = []
virus_url = None

@outerFunction
def get_full_data(headers):
    """获取parent_id中所有的数据"""
    global full_data
    logger.info('info - decorate function')
    for url in urllist:
        result = requests.get(url, headers=headers, verify=False)
        res = json.loads(result.content.decode())['children']
        full_data.extend(res)
        logger.info(f'GET {url} {result.status_code} - the message already add to full data')


def manager():
    """提取出需要统计的单位数据"""
    global filter_data
    try:
        result = get_unit()
        get_full_data()
        filter_data = [[item['id'], item['name'], item['sum'], item['count']] for item in full_data if item['name'] in result]
        return filter_data
    except Exception as e:
        logger.error(f'ERROR - {e}')


def device_data():
    """获取未处理风险数的总数"""
    global filter_data
    manager()
    for item in filter_data:
        url = f"https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id={item[0]}&keywords=&online_status=&%24virusRange=unfix&modulename=device-virus&currentPage=1&pageSize=5000"
        url2 = f"https://10.201.20.10/api/device/show?sorter=id%3Adescend&group_id={item[0]}&keywords=&online_status=&%24deviceRange=unfix&modulename=device-vul&currentPage=1&pageSize=5000"
        with open(temp_path, 'r') as fh:
            headers = json.load(fh)

        try:
            response = requests.get(url, headers=headers, verify=False)
            response2 = requests.get(url2, headers=headers, verify=False)

            # 将未处理风险终端数和未修复漏洞的终端数更新追加入fulldata
            item.append(json.loads(response.content.decode())['pagination']['total'])
            item.append(json.loads(response2.content.decode())['pagination']['total'])
            logger.info(f"GET {url} {response.status_code} - Success virus device number add to filter data")
            logger.info(f"GET {url2} {response.status_code} - Success vuln device number add to filter data")
            logger.info(f"progress: {filter_data.index(item) + 1}/{len(filter_data)}")

        except Exception as e:
            logger.error(f'ERROR - {e}')


def get_CooperativeUnits():
    """获取合作单位"""
    global filter_data
    with open(cooperativeunits_path, 'r', encoding='utf8') as fh:
        contents = fh.readlines()
    res = [item.replace('\n', '') for item in contents]
    for item in filter_data:
        if item[1] in res:
            item.append("是")
        else:
            item.append("否")

def output(data, columns):
    """输出数据"""
    df = pd.DataFrame(data, columns=columns)

    InstallDetail_path = os.path.join(data_path, 'InstalltionDetail')
    file_name = "{}.csv".format(datetime.datetime.now().strftime("御点安装明细_%Y_%m_%d_%H_%M_%S"))
    csv_file_path = os.path.join(InstallDetail_path, file_name)
    df.to_csv(csv_file_path, index=False, encoding='utf-8')
    logger.info(f"SUCCESS OUTPUT {csv_file_path}")

def run():
    """程序结束"""
    device_data()
    get_CooperativeUnits()
    try:
        columns = ['单位ID', '单位名称', '设备总数', "实名安装数", "未处理风险终端数", "未修复漏洞终端数", "是否为合作单位"]
        c1, c2, c3 = 0, 0, 0
        v1, v2, v3 = 0, 0, 0
        k1, k2, k3 = 0, 0, 0
        for item in filter_data:
            if item[1] == '中国xxx分公司':
                item[1] = "xx区域总部"
            if item[1] == "中国xx分公司":
                item[1] = "xx总部"
            if item[1] == "中国xx公司":
                item[1] = "xx总部"
            if item[1] == "中国xx分公司":
                item[1] = "xx总部"
            if item[1] == "中国xx分公司":
                item[1] = "x事业部"
            if item[1] == "xx分公司":
                item[1] = "xx事业部"
            if item[1] == "xx分公司":
                item[1] = "xx事业部"
            if item[1] == "中国xx分公司":
                item[1] = "xx总部"
            if item[1] == "中国xx分公司":
                item['1'] = "xx总部"
            if item[1] == "xx局":
                c1 = c1 + item[3]
                v1 = v1 + item[4]
                k1 = k1 + item[5]
            if item[1] == "xx局":
                c2 = c2 + item[3]
                v2 = v2 + item[4]
                k2 = k2 + item[5]
            if item[1] == "xx局":
                c3 = c3 + item[3]
                v3 = v3 + item[4]
                print(v3)
                k3 = k3 + item[5]
            if item[1] == "xx":
                item[3] = item[3] - c1 - c2 - c3
                item[4] = item[4] - v1 - v2 - v3
                item[5] = item[5] - k1 - k2 - k3


        output(filter_data, columns)
    except Exception as e:
        logger.error(f'ERROR - {e}')



if __name__ == '__main__':
    run()

