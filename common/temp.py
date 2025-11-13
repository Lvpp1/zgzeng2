#! /usr/bin/env python
# --*--coding: utf8


import common.login_demo as common
import json
import logging

logger = logging.getLogger('my_logger')

#装饰器
def outerFunction(func):

    def innerFunction(*args):
        try:
            with open(common.temp_path, 'r') as fh:
                headers = json.load(fh)
            func(headers=headers, *args)
            logger.info(f"SUCCESS - GET HEADEAR")

        except Exception as e:
            logger.warning('warning - Cache headers have expired, generating new headers')
            obj = common.TencentYdLogin()
            obj.run()
            headers = obj.headers
            func(headers=headers, *args)
        return headers


    return innerFunction




