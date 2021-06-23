from os import path

import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库

# 准备词云所需的文字（词）
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
    # print(item[0])
# print(text)
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))

img = Image.open(r'./static/assets/img/tree.jpg')  # 打开遮罩图片

img_array = np.array(img)  # 将图片转换为数组
# print(string)
wc = WordCloud(

    background_color="white",  # 背景色为白色
    mask = img_array,  # 添加蒙版
    font_path="/System/Library/fonts/PingFang.ttc"
)
wc.generate_from_text(string)
print('打开成功')
# wc.generate(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴

plt.show()  # 显示生成的词云图片

# 输出词云图片到文件
# pd = path.dirname(__file__)
# # os.path.join()：  将多个路径组合后返回
# wc.to_file(path.join(pd, "h11.jpg"))
# plt.savefig(r'./static/assets/img/word.jpg',dpi=500)
