# -*- coding: utf-8 -*-

"""
@Version : Python3.6
@Time    : 2018/10/6 13:07
@File    : demo.py
@SoftWare: PyCharm 
@Author  : Guan
@Contact : youguanxinqing@163.com
@Desc    :
=================================
    对影评可视化
=================================
"""
import pymongo
import numpy as np
import pandas as pd
from PIL import Image
from pyecharts import Pie
from pyecharts import Geo
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

from CONFIG import *


class AnalysisTool(object):
    """实现可视化的工具"""
    def create_wordcloud(self, text):
        """生成词云"""
        # 对图片做处理
        maskPic = np.array(Image.open(IMAGE_PATH))

        # 停用词
        stopwords = STOPWORDS.copy()
        words = ["其次", "不錯看", "其实"]
        list(map(stopwords.add, words))

        wordcloud = WordCloud( font_path=TTF_PATH, # 字体路径（中文字需要添加）
                               width=500,
                               height=400,
                               stopwords=stopwords,
                               max_font_size=100,
                               random_state=30,
                               min_font_size=10,
                               background_color="white").generate(text.replace("\n", ""))

        # 改变字体颜色
        img_colors = ImageColorGenerator(maskPic)
        # 字体颜色为背景图片的颜色
        wordcloud.recolor(color_func=img_colors)
        # 生成图片并保存
        img = wordcloud.to_image()
        img.save(SAVE_IMAGE_PATH)
        print("词云图【成功】")

    def create_pie(self, attr, value):
        """生成圆饼图"""
        pie = Pie("评分-人数占比图")
        pie.add(
            "", attr, value,  # 图例名（不使用图例）
            radius=[40, 75],  # 环形内外圆的半径
            is_label_show=True,  # 是否显示标签
            label_text_color=None,  # 标签颜色
            legend_orient='vertical',  # 图例垂直
            legend_pos='right'
        )
        pie.render(PIE_PATH)
        print("圆饼图【成功】")

    def create_map(self, city, value, name="观影地区分布"):
        """Scatter类型地图"""

        geo = Geo(name, "数据来源于猫眼",
                  title_color="#fff", title_pos=
                  "center", width=800, height=500,
                  background_color='#404a59')
        # 添加城市坐标
        geo.add_coordinate_json(CITY_JSON_FILE)
        geo.add("", city, value, is_label_show=True, is_roam=True,
                visual_range=[0, 40],
                visual_text_color="#fff",
                symbol_size=15, is_visualmap=True)
        geo.render(MAP_PATH)
        print("地理分布图【成功】")


class Creation(object):
    """主要实现数据清洗以及
    生成需要的目标文件"""
    def __init__(self, collection):
        self.collection = collection
        self.at = AnalysisTool()
        self.data = self.get_tuple(self.collection.find())

    def get_tuple(self, lyst):
        """格式化列表"""
        return [tuple(item.values()) for item in lyst]

    def all_contents(self):
        """对所有评论生成词云"""
        contents = [item[3] for item in self.data]
        self.at.create_wordcloud("".join(contents))

    def score_accounting(self):
        """不同分数，对应占比"""
        scores = [item[2] for item in self.data]
        frame = pd.DataFrame(scores, columns=["score"])
        scorePerson = dict(frame["score"].value_counts())

        attr = [str(item) for item in scorePerson]
        value = list(scorePerson.values())
        self.at.create_pie(attr, value)

    def distinguish_by_city(self):
        """观影城市分布"""
        cities = [item[4] for item in self.data]
        frame  = pd.DataFrame(cities, columns=["city"])
        cityPerson = dict(frame["city"].value_counts())
        # 许多小地方坐标无法识别，故清洗
        cleanedData = {key:cityPerson[key] for key in cityPerson if cityPerson[key]>5}

        city = list(cleanedData.keys())
        value = list(cleanedData.values())
        self.at.create_map(city, value)

    def bad_comments(self):
        """以低于3分为标准，认为是差评, 保存指定txt文本中"""

        # 数据过滤，只保留差评
        badComments = [(item[2], item[3]) for item in self.data if item[2]<3]
        # 对差评排序
        sortedComments = sorted(badComments, key=lambda item: item[0])
        # 写入txt文件
        with open(BAD_COMMENTS_TXT, "w", encoding="utf-8") as file:
            for comment in sortedComments:
                file.write("{}\n".format(str(comment)))


if __name__ == "__main__":
    # MongoBD的配置
    client = pymongo.MongoClient("localhost", 27017)
    db = client.move_comments
    collection = db.cry_me_a_sad_river

    creation = Creation(collection)
    creation.all_contents()
    creation.score_accounting()
    creation.distinguish_by_city()
    creation.bad_comments()