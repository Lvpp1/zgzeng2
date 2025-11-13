#! /usr/bin/env python
# --*--coding: utf8

import logging
import requests
from moudle import InstallationDetails,GetCore,FullData,DisplayID,GetVirusDate,GetVulDate,GetNetworkAttackDetail
import argparse


requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')
def help_information():
    title = """
      __                                     __               .___
_/  |_  ____   ____   ____  ____   _____/  |_   ___.__. __| _/
\   __\/ __ \ /    \_/ ___\/ __ \ /    \   __\ <   |  |/ __ | 
 |  | \  ___/|   |  \  \__\  ___/|   |  \  |    \___  / /_/ | 
 |__|  \___  >___|  /\___  >___  >___|  /__|    / ____\____ | 
           \/     \/     \/    \/     \/        \/         \/ 
           
    
    """
    print(title)
    print(
    """
    获取各单位评分情况:              python run.py -c 
    获取展示各二级单位 ID:           python run.py -s
    获取各单位实名用户终端:           python run.py -i
    获取安装御点全量数据详情:         python run.py -a
    获取未处理风险涉及的终端:         python run.py -g
    获取未修复漏洞涉及的终端:         python run.py -v
    获取网络攻击涉及终端详情:         python run.py -n 20240101 20240102   
    """
    )


parser = argparse.ArgumentParser(description="腾讯御点各数据获取参数")
parser.add_argument("-c", "--core", action="store_true", help="获取各单位评分情况")
parser.add_argument("-s", "--show", action="store_true", help="展示各二级单位ID")
parser.add_argument("-a", "--all", action="store_true", help="获取全集团安装御点的用户详情")
parser.add_argument("-g", "--virus", action="store_true", help="获取未处理风险涉及的终端")
parser.add_argument("-v", "--vuls", action="store_true", help="获取未修复漏洞涉及的终端")
parser.add_argument("-i", "--installdetail", action="store_true", help="获取各单位实名用户终端")
parser.add_argument('-n', '--GetAttack', nargs=2, metavar=('START_DATE', 'END_DATE'), help='获取网络攻击涉及终端详情 参数格式:20241001, 例如python run.py -n 20241001 20241001')

help_information()
args = parser.parse_args()
logger.info("STARTING PROCESS...")
if args.core:
    GetCore.run()
elif args.show:
    DisplayID.run()
elif args.all:
    obj = FullData.FullDate()
    obj.run()
elif args.virus:
    GetVirusDate.run()
elif args.vuls:
    GetVulDate.run()
elif args.GetAttack:
    GetNetworkAttackDetail.set_datas(args.GetAttack[0], args.GetAttack[1])
    GetNetworkAttackDetail.run()
elif args.installdetail:
    InstallationDetails.run()

