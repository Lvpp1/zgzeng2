#! /usr/bin/env python
# --*--coding: utf8

import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from colorlog import ColoredFormatter


relative_path = pathlib.Path(__file__).parent.parent
logs_relative_path = relative_path.joinpath('logs')


def setup_logging(*args):
    """日志设置"""
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # 创建终端处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # 设置终端输出日志级别
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s %(filename)s:%(lineno)d %(message)s',
    ))
    log_file = os.path.join(logs_relative_path, 'app.log')
    # 创建按天切割的文件处理器
    file_handler = TimedRotatingFileHandler(
        log_file,  # 日志文件名
        when='midnight',  # 每天午夜切割日志文件
        interval=1,  # 间隔时间（1天）
        backupCount=7  # 保留最近7个日志文件，超出将被删除
    )
    file_handler.setLevel(logging.DEBUG)  # 设置文件输出日志级别
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s %(filename)s:%(lineno)d %(message)s'
    ))

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# 调用 setup_logging() 函数以初始化日志配置
# setup_logging()

