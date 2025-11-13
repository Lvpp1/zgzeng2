import json
import requests
from common.temp import outerFunction
import logging
import pathlib
import os
import pandas as pd
import datetime
from collections import Counter


requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')
parent_path = pathlib.Path(__file__).parent.parent
temp_path = os.path.join(parent_path, 'temp')
data_path = os.path.join(parent_path, 'data')
attack_data_mid_list = []
attack_data = []
start_date = None
end_date = None
total = None


def set_datas(start, end):
    """输入时间参数"""
    global start_date, end_date
    start_date = start
    end_date = end


@outerFunction
def get_attack_total_number(headers):
    """获取网络攻击数量"""
    global total
    url = f"https://10.201.20.10/api/report/query?sorter=report_time%3Adescend&group_id=1&date_begin={start_date}000000&date_end={end_date}235959&tableId=attack%2Fterminal%2Fdetail&between=report_time&modulename=attack-stat&role=0&currentPage=1&pageSize=10"
    try:
        response = requests.get(url, headers=headers, verify=False)
        total = json.loads(response.content.decode())['pagination']['total']
        logger.info(f"GET {url} {response.status_code}")
    except Exception as e:
        logger.info(f"ERROR - {e}")


def get_pages(total):
    """获取网络攻击总数显示页数"""
    try:
        if isinstance(total / 5000, int):
            pages = total / 5000 + 1
        elif isinstance(total / 5000, float):
            pages = int(total / 5000) + 2
        return pages
    except Exception as e:
        logger.error(f"ERROR - {e}")


def get_headers():
    """获取临时temp存储的请求头"""
    with open(temp_path, 'r') as fh:
        headers = json.load(fh)
    return headers


def get_network_attack_data(page):
    """获取攻击日志数据"""
    global attack_data_mid_list,attack_data
    try:
        headers = get_headers()
        url = f"https://10.201.20.10/api/report/query?sorter=report_time%3Adescend&group_id=1&date_begin={start_date}000000&date_end={end_date}235959&tableId=attack%2Fterminal%2Fdetail&between=report_time&modulename=attack-stat&role=0&currentPage={page}&pageSize=5000"
        response = requests.get(url, headers=headers, verify=False)
        attack_data = json.loads(response.text)['list']
        logger.info(f"GET {url} {response.status_code}")
        for item in range(len(attack_data)):
            attack_data_mid_list.append(attack_data[item]['mid'])
        return attack_data_mid_list, attack_data
    except Exception as e:
        logger.error(f"ERROR - {e}")


def unique_info(network_attack_data):
    """去重"""
    tuple_list = [tuple(item) for item in network_attack_data]
    counter = Counter(tuple_list)
    unique_list_with_count = [[list(item), count] for item, count in counter.items()]
    unique_network_attack_list = []
    for ite in unique_list_with_count:
        new_list = ite[0] + [ite[1]]
        unique_network_attack_list.append(new_list)
    return unique_network_attack_list


def query_group_name(mid):
    """获取涉及终端人员的组织架构"""
    headers = get_headers()
    query_url = 'https://10.201.20.10/api/device/show?sorter=id%3Adescend&modulename=device-info&online_status=0&others%5Bfield%5D=mid&others%5Bvalue%5D={}'.format(mid)
    try:
        response = requests.get(query_url, headers=headers, verify=False)
        group_name_path = json.loads(response.content.decode())['list'][0]['group_name_path']
        logger.info(f"GET {query_url} {response.status_code}")
    except:
        group_name_path = ''
    return group_name_path


def output(data):
    """输出报告"""
    try:
        columns = ['终端MID', '姓名', '攻击类型', "攻击次数", "组织架构"]
        df = pd.DataFrame(data, columns=columns)
        NetworkAttackDetail_path = os.path.join(data_path, 'NetworkAttackDetail')
        file_name = "{}.csv".format(datetime.datetime.now().strftime("御点_%Y_%m_%d_%H_%M_%S"))
        csv_file_path = os.path.join(NetworkAttackDetail_path, file_name)
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        logger.info(f"OUTPUT SUCCESS {csv_file_path}")
    except Exception as e:
        logger.info(f"ERROR - {e}")


def run():
    """执行入口"""
    global network_attack_data_list
    get_attack_total_number()
    pages = get_pages(total)
    for page in range(1, pages):
        get_network_attack_data(page)
    network_attack_data = []
    for item in attack_data:
        network_attack_data.append([item['mid'], item['name'], item['vulid']])
    unique_network_attack_list = unique_info(network_attack_data)
    network_attack_data_list = []
    for item in unique_network_attack_list:
        mid = item[0]
        group_path_name = query_group_name(mid)
        network_attack_data_list.append(item + [group_path_name])
    for item in network_attack_data_list:
        if "未分组" in item[4] or "离职和报废终端" in item[4]:
            network_attack_data_list.remove(item)
    output(network_attack_data_list)


