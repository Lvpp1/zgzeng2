#! /usr/bin/env python
# --*--coding: utf8

import time
import ddddocr
import requests
import os
import datetime
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
import pathlib
import logging
import json
import re
from common.my_logging import setup_logging

setup_logging()
requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')
code_directory = pathlib.Path(__file__).parent.parent.joinpath('code_dir')
temp_path = os.path.join(pathlib.Path(__file__).parent.parent, "temp")


class TencentYdLogin:
    """腾讯御点登录"""

    def __init__(self):
        self.username = 'admin'
        self.password = "FIWgKu2e11/xgPfN8mo6cUXS34lA+VBhJWSJq0tBkUBQ7Dob6hxSfkpW+2/DphCM628UXujUVo3GIZXvuQvAARKg6vwc+un1u6ppUfi79AFM8aAgpdHsRw20rNbqZTcP2/6gboc3vwbA7sUBjTlejYfT8yd7jVkQO62ebz8awI7iD3RH826aJVzXo7FVS+pmg1HuyPzJsR7ppO/D5tV705pB0rG1xxXScSfB3iLncNlcfyI452l5tOXNq6pCN/DZlm6CwlujLq/JRF/RTXD9KjBTCWHCL/ynQiQ/Tia0BF6p+GXqoquDkV3ZoX74s0Y4TrdsgtIY08iyl6Ib/qRJTQ1C1+wUyujlHmX50VsNZaYtMA+aHcLeTplr57rR4ZX2/d55W2mkK9FBkT+3u7zxrtCVv+b+MOtKOQq6cPNx3FDP3NStAzkPoYZGH0bQZoPo2ehI97jqI/g9JWjOdQf/R0fJW1uk8Q6tl/ZIv8c/0vhNuJSXPIg9eMsydQoG5ct6JSJFIgiRV5Zxq86iBlJ7QCGlpX8oPgYFh8W2SOuAoZ0tpMcWWkSw73fcF/fTdu/TVH4GHLyr45ZtIPLT2/vn1SHrHtPdXScT3bNid1WP7tu4K8rfeRimnoGICiQcOgwXSo6WEgLwGTokk5mR6t3rCOj1/kF7/254VUPOziSe3ZU="
        self.svg_verify_url = f"https://10.201.20.10/api/verify?_t={int(time.time()*1000)}"
        self.login_url = "https://10.201.20.10/user/login"
        self.code_directory_path = os.path.dirname(os.path.dirname(__file__)) + "\\code_dir"
        self.pcmgr_session = None
        self.svg_header = {
            "Host": "10.201.20.10",
            "Referer": "https://10.201.20.10/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 GooBrowser/100.0.0.21",
        }
        self.log_headers = {
            "Host": "10.201.20.10",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 GooBrowser/100.0.0.21"
        }
        self.data ={
            "username": f"{self.username}",
            "password": f"{self.password}",
        }
        self.headers = {
            "Host": "10.201.20.10",
            "Referer": "https://10.201.20.10/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 GooBrowser/100.0.0.21",
        }

    def get_svg_verify(self):
        """获取验证码数据"""
        try:
            resp = requests.get(url=self.svg_verify_url, headers=self.svg_header, verify=False)
            resp_ = resp.headers['Set-Cookie'].split(";")

            # 获得session值
            for i in range(len(resp_)):
                if "pcmgr_session" in resp_[i]:
                    pcmgr_session = resp_[i].split("=")[1]
            conts = resp.content.decode()

            # 获取svg代码
            filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.svg'
            with open(rf"{os.path.join(self.code_directory_path, filename)}", "w", encoding="utf8") as f:
                f.write(conts)
            self.pcmgr_session = pcmgr_session
            self.log_headers.update({"Cookie": f"pcmgr_session={self.pcmgr_session}"})
            logger.info(f"GET {self.svg_verify_url} Success - saving svg file {filename}")
            return os.path.join(code_directory, filename)

        except Exception as e:
            logger.error(f'Error - {str(e)}')


    def get_png(self, filename):
        """转化识别验证码"""
        # 转化
        logger.info('Conversion recognition verification code')
        drawing = svg2rlg(filename)
        renderPM.drawToFile(drawing, f"{filename}.png", fmt="PNG")

        # 识别
        try:
            with open(f"{filename}.png", "rb") as f:
                image = f.read()
            res = ddddocr.DdddOcr(old=True).classification(image)
            self.data.update({"code": f"{res}"})
            logger.info(f'SUCCESS - Verification code recognition result:{res}')

        except Exception as e:
            logger.error('ERROR - Verification code error')


    def login(self):
        """登录逻辑"""
        login_res = requests.post(self.login_url, headers=self.log_headers, data=self.data, verify=False)
        cookie_string = login_res.headers['Set-Cookie']
        pattern = r'pcmgr_check=([^;]+);|pcmgr_session=([^;]+);'
        matches = re.findall(pattern, cookie_string)

        # 提取值
        pcmgr_check = matches[0][0] if matches[0][0] else None
        # pcmgr_session = matches[1][1] if matches[1][1] else None

        self.headers.update({"Cookie": f"pcmgr_session={self.pcmgr_session}; pcmgr_check={pcmgr_check}; pcmgr_loginname=admin; topNotice_Free_noever=1",
        "csrfToken": f"{pcmgr_check}",})
        return login_res.content.decode()

    def run(self):
        """自动化循环登录逻辑"""
        login_status = False
        while login_status != True:
            try:
                login_status = self.login()
                filename = self.get_svg_verify()
                self.get_png(filename)
                result = self.login()
                # print(json.loads(result))
                if json.loads(result)["success"]:
                    login_status = True
                    logger.info(f'POST {self.login_url} success - login success')

                    # 自动清除
                    if os.name == 'nt':
                        os.popen(f"del {code_directory}\*.svg")
                        os.popen(f"del {code_directory}\*.png")

                    # 将请求头存入到temp临时存储
                    try:
                        with open(temp_path, 'w', encoding="utf8") as fh:
                            json.dump(self.headers, fh, ensure_ascii=False, indent=4)
                            logger.info('success - headers写入成功')
                    except Exception as e:
                        logger.error(f'Error - {str(e)}')
                else:
                    logger.warning('Fail - verification code error')

            except Exception as e:
                logger.error(f'Error - {str(e)} invalid username or password')






