# -*- coding: utf-8 -*-

"""
@Version : Python3.6
@Time    : 2018/10/6 11:04
@File    : CONFIG.py
@SoftWare: PyCharm 
@Author  : Guan
@Contact : youguanxinqing@163.com
@Desc    :
=================================
    配置信息
=================================
"""

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) "
                   "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 "
                   "Mobile/15A372 Safari/604.1")
}

COMMENT_URL = "http://m.maoyan.com/mmdb/comments/movie/1217236.json"

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TTF_PATH = "{}/source/FZLTXIHK.TTF".format(BASE_DIR)
IMAGE_PATH = "{}/source/luoluo4.jpg".format(BASE_DIR)
SAVE_IMAGE_PATH = "{}/html/wordcloud_img.jpg".format(BASE_DIR)
PIE_PATH = "{}/html/pie.html".format(BASE_DIR)
MAP_PATH = "{}/html/map.html".format(BASE_DIR)
CITY_JSON_FILE = "{}/source/cityDatas.json".format(BASE_DIR)
BAD_COMMENTS_TXT = "{}/html/badComments.txt".format(BASE_DIR)
