#! /usr/bin/env python
# --*--coding: utf8


import json
import requests
from common.temp import outerFunction
import logging


requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')


class GetUnitId:
    """获取各单位的id"""
    def __init__(self):
        self.parent_id = [1, 238688, 302955, 242753]
        self.urllist = ['https://10.201.20.10/api/group/orgChildGroup?sorter=id%3Aasc&parent_id={}'.format(item) for item in self.parent_id]
        self.headers = None
        self.info = []


    @outerFunction
    def func(self, headers):
        """针对self.url发出请求获取响应"""
        logger.info('info - decorate function')
        for url in self.urllist:
            result = requests.get(url, headers=headers, verify=False)
            res = json.loads(result.content.decode())['children']
            self.info.extend(res)
            logger.info(f'GET {url} {result.status_code} - the message already add to info')


    @classmethod
    def get_unit(cls):
        """获取所有单位名称,存放在列表中"""
        result = []
        try:
            with open('company', 'r', encoding='utf8') as fh:
                contents = fh.readlines()
            for item in contents:
                if '-' in item:
                    result.append(item.split('-')[1].replace('\n', ''))
                elif '\n' in item:
                    result.append(item.replace('\n', ''))
                else:
                    result.append(item)
            return result
        except Exception as e:
            logger.error(f'error - {e}')

    def run(self):
        result = GetUnitId.get_unit()
        self.func()
        try:
            res = [item for item in self.info if item['name'] in result]
            with open('UnitInfo.txt', 'w', encoding='utf8') as fh:
                json.dump(res, fh, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f'error - {e}')



if __name__ == '__main__':
    obj = GetUnitId()
    obj.func()

