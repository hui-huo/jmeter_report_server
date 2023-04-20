# _*_ coding: utf-8 _*_
"""
Time:     2023/3/31 16:02
Author:   Hui Huo.
File:     utils.py
Describe: 
"""

import uuid
from datetime import datetime


def generate_unique_id():
    # 使用UUID4方式生成唯一ID
    uid = uuid.uuid4().hex
    # 截取前8位作为ID
    unique_id = uid[:8]
    return unique_id


def transition_time(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    timestamp = int(date_obj.timestamp()) * 1000
    return timestamp
