# -*- coding: utf-8 -*-

"""
@Version : Python3.6
@Time    : 2018/10/6 11:07
@File    : spider.py
@SoftWare: PyCharm 
@Author  : Guan
@Contact : youguanxinqing@163.com
@Desc    :
=================================
    爬取猫眼影评（悲伤逆流成河）
=================================
"""
import time
import pymongo
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from CONFIG import *


class Offset(object):
    """生成偏移量，使其能够包含边界数"""
    def __init__(self, left, right, step):
        self.left = left
        self.right = right
        self.step = step
        self.count = left

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= self.right:
            num = self.count
            self.count += self.step
        elif (self.right+self.step) > self.count > self.right:
            num = self.right
            self.count += self.step
        else:
            raise StopIteration

        return num


def get_comments(url, params, tries=3):
    """获取评论"""
    try:
        response = requests.get(url, params=params, headers=HEADERS)
    except requests.HTTPError:
        if tries<=0:
            return None
        else:
            get_comments(url, params, tries-1)
    else:
        return response.json()

def extract_data(data):
    """提取数据"""
    cmts = data.get("cmts")
    if not cmts:
        print("get total 0")
        return None
    for cmt in cmts:
        yield {
            "_id": cmt["userId"],
            "nickName": cmt["nickName"],
            "score": cmt["score"],
            "content": cmt["content"],
            "cityName": cmt["cityName"],
            "time": cmt["time"],
        }

def save_to_mongo(data):
    """数据存储至mongo"""
    collection.save(data)
    print("【插入成功】{}".format(data))

def main(offset):
    PARAMS = {
        "_v_": "yes",
        "offset": offset,
        "startTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 2018-10-06 10:56:47
    }
    commentsData = get_comments(COMMENT_URL, PARAMS)

    if commentsData:
        for item in extract_data(commentsData):
            save_to_mongo(item)


if __name__ == "__main__":
    # 配置mongodb
    start = time.time()
    client = pymongo.MongoClient("localhost", 27017)
    db = client.move_comments
    collection = db.cry_me_a_sad_river

    FAILURE_URLS = list()
    # 线程池
    with ThreadPoolExecutor(max_workers=20) as pool:
        pool.map(main, Offset(0, 1000, 15))

    print("失败链接集合：{}".format(FAILURE_URLS))
    print("一共花费时间：{}".format(time.time()-start))