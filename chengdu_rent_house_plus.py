#!/usr/bin/env python
# coding: utf-8

# # 期末作业

# ## 1. 背景描述

# 2021年5月13日，教育部高校学生司司长王辉在新闻发布会上指出2021届全国普通高校毕业生总规模将首次突破900万，达到909万，和2020年的874万的毕业生人数相比，同比增加35万，2021年全国高校毕业生人数再次创下新高。同时，叠加新冠肺炎及归国留学生的归国潮影响，2021年就业市场依然面临不小挑战。对于走出象牙塔的学子们而言，就业时不得不做一道选择题—选择在哪里就业：家乡、一线及新一线城市、家乡所在省会城市还是毕业院校所在城市？
# 
# 根据贝壳研究院发布的《毕业季租房洞察报告》显示，2021届毕业生在一线城市广州、上海北京及深圳的就业人数最多，新一线城市中成都、南京、郑州、杭州及武汉成为毕业青年的首选就业城市。凭借着无可取代的优质资源及产业基础，一线城市仍是毕业青年首选的就业目标城市。本文以成都市为例，使用Python爬取了成都市的租房数据，希望可以为未来想要在成都市就业的同学们，提供一些关于租房的有价值的信息。
# 
# 

# ## 2. 数据获取

# ① 利用requests库对贝壳租房网进行数据爬取
#    
# ② 由于爬取过多数据页面会导致爬虫被中止，为了保证爬虫能够数据能够正常运行，设置爬取页面为50页

# In[1]:


import time
import requests
from lxml import html
import json
import re


# 爬虫
class House(object):
    def __init__(self):
        self.start_url = "https://cd.zu.ke.com/zufang"
        self.url_temp = "https://cd.zu.ke.com/zufang/pg{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Cookie": "lianjia_uuid=591aa9ef-0af5-4b49-96a9-c9334074346e; select_city=510100; lianjia_ssid=7e19b7b6-8cb6-43a2-9e3a-0383572a17d5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221788ca6dbd4a6-04db4049139cda-57442618-1327104-1788ca6dbd5ae4%22%2C%22%24device_id%22%3A%221788ca6dbd4a6-04db4049139cda-57442618-1327104-1788ca6dbd5ae4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fs%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%7D%7D; login_ucid=2000000176709570; lianjia_token=2.001046bd6277458f4c01eb94530e9c3f47; lianjia_token_secure=2.001046bd6277458f4c01eb94530e9c3f47; security_ticket=bKvzfpXspbqEHd4t09bWj8x+fNkp5USo3xIVZw26xpWpvndPeJtODHwL8dMA0KevZjlwtVKt6GDjz7gRCxmo6WNaf/sOcxQw8p2O2cygWXubbjeaKvL0E3Qmemm5KKSMYF58iZhvB/VglF0bxMG9z1UOP66I+C1bDq+QDZXubpY=; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNDA3YTk2MDM2MWU0ZTIxYzA2YmUwNzA2MjFiYWMwZmNiYzM1N2MxMzEwZDQ2ODliYjQ3ZDI2NmRiMDlhOTYyZGUxMjZjNWQ3MDM5ODZjZWFkMzVjZWQyNmU2ZjM2Y2IyODMyYWVjMmYyM2VhNWNlOTYxNGY5ODBlOGNhNjEwN2QzMmRkMmRkYjk5MTZhMmVkODQ1MDg0Y2I2N2I1NTRhM2Y4ZjM4YWY4YmRiZTRhNzJjN2ExMWEyMTUwMjQ5ZTAxNDliMGM1NDI3YmY3ODRkOWU4Yzk4NTAwNTExMWQ4OTIyYTNiOGU1YmE5MGY5NzAxNjllODIzMGNhOTliMTUxYTYwM2FhNjU1MmJkNjc0OTBkYjZhZGFmMTQ1MzkzNjc0MjBiNzUyY2E4NDJjNjA3MTg4NzY3NWE4MTc5ZWQwODA1Zjk1Njc4ZmMzNGYxYjJiZDI4ZWI0YWIwZWMzZjBlYlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiNTBkMmJmMFwifSIsInIiOiJodHRwczovL2NkLnp1LmtlLmNvbS96dWZhbmcvcGcyLz9zaG93TW9yZT0xIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0="
        }

    # 构造请求所需的url列表
    def get_url(self, page):
        url_list = [self.url_temp.format(i) for i in range(1, page + 1)]
        return url_list

    # 发送http请求并获取响应数据
    def parse(self, url):
        rest = requests.get(url, headers=self.headers)
        return rest.text

    # 获取列表页数据
    def get_content_list(self, rest):
        time.sleep(0.5)
        html_rest = html.etree.HTML(rest)
        divs = html_rest.xpath('//div[@class="content__list"]/div')
        item_list = []
        for i in divs:
            item = {}
            a = i.xpath('./a/@href')
            item["home_url"] = "https://cd.zu.ke.com/" + a[0]
            home_position = i.xpath(
                '//div[@class="content__list"]/div//p[@class="content__list--item--des"]/a[1]/text()')
            item["home_position"] = home_position[0] if len(home_position) > 0 else "未知"
            item = self.parse_detail(item["home_url"], item)
            item_list.append(item)

        return item_list

    # 获取详情页数据
    def parse_detail(self, detail_url, item):
        time.sleep(0.2)
        rest = self.parse(detail_url)
        rest_html = html.etree.HTML(rest)
        home_price = rest_html.xpath('//div[@class="content__aside--title"]/span/text()')
        item['home_price'] = home_price[0] if len(home_price) > 0 else "未知"
        home_mode = rest_html.xpath('//ul[@class="content__aside__list"]/li[2]/text()')
        item['home_mode'] = home_mode[0].strip().split(" ")[0] if len(home_mode) > 0 else "未知"
        home_layer = rest_html.xpath('//ul[@class="content__aside__list"]/li[3]/span[2]/text()')
        item['home_layer'] = home_layer[0].strip().split(" ")[1].split("/")[0] if len(home_layer) else "未知"
        home_toward = rest_html.xpath('//ul[@class="content__aside__list"]/li[3]/span[2]/text()')
        item['home_toward'] = home_toward[0].strip().split(" ")[0] if len(home_toward) else "未知"
        home_area = rest_html.xpath('//ul[@class="content__aside__list"]/li[2]/text()')
        item['home_area'] = home_area[0].strip().split(" ")[1] if len(home_area) else "未知"
        is_lift = rest_html.xpath('//div[@class="content__article__info"]/ul/li[contains(text(),"电梯")]/text()')
        item['is_lift'] = is_lift[0].split("：")[1] if len(is_lift) > 0 else "未知"
        return item

    # 保存数据
    def save(self, content):
        with open('成都租房.json', 'w', encoding='utf-8') as f:
            json.dump(content, fp=f, ensure_ascii=False, indent=2, sort_keys=True)
        print('数据已保存至json文件中')

    # 主程序
    def run(self):
        url_list = self.get_url(50)
        item_list = []
        for url in url_list:
            # 打印url，获知爬取进度
            print(url)
            rst = self.parse(url)
            items = self.get_content_list(rst)
            item_list.extend(items)
        content = {"items": item_list}
        self.save(content)


# house = House()
# house.run()

# ## 3. 数据预处理

# ① 将json格式转为csv格式
# 
# ② 将数据中值为未知的异常记录删除
# 
# ③ 为了后文统计分析方便，选择将同一房屋有多个朝向的记录也一并删除

# In[2]:


from pyecharts.globals import CurrentConfig, NotebookType, ThemeType
import warnings

warnings.filterwarnings('ignore')
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
CurrentConfig.ONLINE_HOST = 'https://assets.pyecharts.org/assets/'
import re
import numpy as np
import pandas as pd
from pyecharts.charts import Pie, Bar, Polar, Funnel, Scatter
import pyecharts.options as opts
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# In[3]:


# 将json格式转换为csv格式
import json
import pandas as pd


def convert_fmt(file_name, cols):
    with open('成都租房.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    data = data['items']
    data = pd.DataFrame(data)
    data.drop(columns=['home_url'], inplace=True)
    data = data[cols]
    data.to_csv(file_name, index=False, encoding='utf-8-sig')
    print('已保存为csv文件')


file_name = 'house.csv'
cols = ['home_position', 'home_price', 'home_mode', 'home_area', 'home_layer', 'home_toward', 'is_lift']
convert_fmt(file_name, cols)

data = pd.read_csv(file_name, header=0, index_col=None)
data.head()


# In[4]:


# 数据预处理
def data_process(df):
    df['home_area'] = df['home_area'].apply(lambda x: float(re.findall('(.*?)㎡', x)[0]) if not x == "未知" else x)
    # 去除数据中带有未知的字段
    # 去除多个朝向的字段
    df['home_position'] = df['home_position'].apply(lambda x: np.nan if x == "未知" else x)
    df['home_price'] = df['home_price'].apply(lambda x: np.nan if x == "未知" else x)
    df['home_mode'] = df['home_mode'].apply(lambda x: np.nan if x == "未知" else x)
    df['home_area'] = df['home_area'].apply(lambda x: np.nan if x == "未知" else x)
    df['home_layer'] = df['home_layer'].apply(lambda x: np.nan if x == "未知" else x)
    df['home_toward'] = df['home_toward'].apply(lambda x: np.nan if x == "未知" or len(re.findall(r'/', x)) > 0 else x)
    df['is_lift'] = df['is_lift'].apply(lambda x: np.nan if x == "未知" else x)
    df = df.dropna()
    return df


file_name = 'house.csv'
# cols = ['home_position', 'home_price', 'home_mode', 'home_area', 'home_layer', 'home_toward', 'is_lift']
# self.convert_fmt(file_name, cols)

df = pd.read_csv(file_name, header=0, index_col=None)
df.head()
df = data_process(df)
print(df.info())
print(df.head())


# ## 4. 统计分析

# ### 4.1 房源分布情况（按区划分）

# ============ 代码 ============

# In[5]:


# 房源分布情况（按区划分）
def diff_house_position(df):
    grouped = df.groupby('home_position')['home_mode'].count().reset_index()
    data = [[i['home_position'], i['home_mode']] for i in grouped.to_dict(orient="records")]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis(
            "房源数量",
            y,
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            title_opts=opts.TitleOpts(title="房源分布情况（按区划分）"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    )
    c.load_javascript()
    return c


data1 = diff_house_position(df)

# ============ 可视化 ============

# In[6]:


data1.render("房源分布情况.html")


# ============ 分析 ============

# 由上图可知，武侯区的租房资源是最多的，其次是高新区和天府新区。武侯区是成都的中心区域，交通便利，物资充裕，因此这里的租房资源自然最多的。而高新区和天府新区是高新技术企业的聚集地，在这个地区就业的人尤其是青年比较多，而青年很可能大多数都是外来人口且经济能力还比较弱，他们的住房需求往往会比较大，因此这两个地区的出租房屋也相对较多。

# ### 4.2  户型统计情况（前十的占比）
# 

# ============ 代码 ============

# In[7]:


# 户型统计情况（前十的占比）
def diff_house_mode(df):
    df['home_mode'] = df['home_mode'].apply(lambda x: re.findall("(.*?)\d卫", x)[0] if not x == "未知" else x)
    grouped = df.groupby('home_mode')['home_area'].count().reset_index().sort_values(ascending=False,
                                                                                     by='home_area')[:10]
    data = [[i['home_mode'], i['home_area']] for i in grouped.to_dict(orient="records")]
    c = (
        Pie()
            .add(
            "",
            data,
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="户型统计情况（前十的占比）"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
    )
    c.load_javascript()
    return c


data2 = diff_house_mode(df)

# ============ 可视化 ============

# In[8]:


data2.render("户型统计情况.html")


# ============ 分析 ============

# 由上图可知，2室1厅、4室1厅、3室1厅的租房户型比较多，这三种户型的租房占比接近50%。由此可见大多数出租房屋还是正常的1厅式，符合家庭住房户型的正常分布情况。同时，没有客厅的租房是非常少的，大多数租房还是有客厅的，毕竟对于工作了一天的打工人而言，客厅是一个住房休息放松的重要场所，出租房屋有无客厅是他们做租房决策时重点考虑的方面，因此为了吸引租客，大多数出租房屋都是具有客厅的。

# ### 4.3  面积统计情况

# ============ 代码 ============

# In[9]:


# 面积统计情况：分为50㎡以下、 50㎡至80㎡ 、80㎡-100㎡ 和100㎡以上这几个部分
def diff_home_area_count(df):
    df = df.query('home_area != "未知"')
    lowwer_50 = len(df.query('home_area<50'))
    bet_50_80 = len(df.query('home_area>=50 & home_area<80'))
    bet_80_100 = len(df.query('home_area>=80 & home_area<100'))
    higher_100 = len(df.query('home_area>=100'))
    data = [['<50㎡', lowwer_50], ["50-80㎡", bet_50_80], ["80-100㎡", bet_80_100], ['>100㎡', higher_100]]
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
            "",
            data,
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="面积统计情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    c.load_javascript()
    return c


data3 = diff_home_area_count(df)

# ============ 可视化 ============

# In[10]:


data3.render("面积统计情况.html")


# ============ 分析 ============

# 由上图可知，大多数出租房屋的面积都集中在50㎡，80㎡以下的出租房屋超过了半数，这说明成都大多数的出租房屋租房面积都比较小，以小面积的租房为主。首先从出租方的角度考虑，因为成都的房价比较高，大多数人没有能力一开始就承担大房子住房贷款的压力，因此他们往往都会选择先买一套面积小一点的住房，导致小面积的租房资源提供得较多。同时，从租赁放的角度考虑，租房的需求方大多是青年，他们的经济负担能力有限，比较愿意租价格较低的住房，而面积和租金一般而言是成正比的，小面积的出租房相对而言价格会更低，这进一步促进了租房市场小面积租房数量的增长。
# 

# ### 4.4 楼层统计情况

# ============ 代码 ============

# In[11]:


# 楼层统计情况
def diff_home_layer_count(df):
    grouped = df.groupby('home_layer')['home_position'].count().reset_index()
    data = [[i['home_layer'], i['home_position']] for i in grouped.to_dict(orient="records")]
    print(grouped)
    c = (
        Funnel(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
            "楼层分布",
            data,
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="楼层统计情况"))

    )
    c.load_javascript()
    return c


data4 = diff_home_layer_count(df)

# ============ 可视化 ============

# In[12]:


data4.render("楼层统计情况.html")


# ============ 分析 ============

# 由上图可知，出租房屋高楼层、中楼层和低楼层分布比较均匀，并没有呈现出较大的差异。相对而言，处于中层的出租房略多一些，大约占总体出租房屋的三分之一。同时，还有极少数的出租房屋是地下室。

# ### 4.5 有无电梯统计情况

# ============ 代码 ============

# In[13]:


def diff_is_lift_count(df):
    grouped = df.groupby('is_lift')['home_position'].count().reset_index()
    data = [[i['is_lift'], i['home_position']] for i in grouped.to_dict(orient="records")]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis(
            "房源数量",
            y,
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            title_opts=opts.TitleOpts(title="有无电梯统计情况"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    )
    c.load_javascript()
    return c


data5 = diff_is_lift_count(df)

# ============ 可视化 ============

# In[14]:


data5.render("有无电梯统计情况.html")


# ============ 分析 ============

# 由上图可知，目前大多数的出租房屋所在楼都安装了电梯。毕竟由于土地的稀缺性，大多数房地产商都选择了建造高层的住房，以提高对土地的利用效率，而高层的楼房为提高居民生活的便利性势必是会安装电梯的。同时，目前人们对生活质量的要求也越来越高，考虑到住户的切实需求，即使楼层不是很高，开发商一般也会选择为楼房安装电梯。因此目前大多数的出租房屋都是具有电梯的。

# ### 4.6 房屋朝向统计情况

# ============ 代码 ============

# In[15]:


def diff_home_toward_count(df):
    grouped = df.groupby('home_toward')['home_position'].count().reset_index()
    data = [[i['home_toward'], i['home_position']] for i in grouped.to_dict(orient="records")]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis(
            "房源数量",
            y,
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            title_opts=opts.TitleOpts(title="房屋朝向统计情况"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    )
    c.load_javascript()
    return c


data6 = diff_home_toward_count(df)

# ============ 可视化 ============

# In[16]:


data6.render("房屋朝向统计情况.html")


# ============ 分析 ============

# 由上图可知，大多数出租房屋的朝向都是坐北朝南（图中有些出租房屋是朝东南或者西南也可以视为朝南），这也符合我国住房朝向的基本情况。我国地处北半球，房子坐北朝南，有利于接受更多阳光照射，日照时间更长。同时，我国属于季风气候，夏季多东南风，冬天为西北风，坐北朝南的房屋可以夏季纳凉风，冬季抵寒冷。最后，从政治文化的角度考虑，我国存在着“南面文化”，统治阶级认为南面是帝王之向，是富贵之向。《易经》中有说道：“圣人南面而听天下，向明而治”，《礼记》中也提到“天子负南向而立。因此我国房屋大多数都是坐北朝南。
# 

# ### 4.7 租金统计情况

# ============ 代码 ============

# In[17]:


# 租金统计情况：分为1000元/月以下 1000元/月-2000元/月  2000元/月-3000元/月 3000元/月以上这几个部分
def diff_home_price_count(df):
    df['home_price'] = df['home_price'].astype(np.int)
    df = df.query('home_price != "未知"')
    lower_1000 = len(df.query('home_price<1000'))
    bet_1000_2000 = len(df.query('home_price>=1000 & home_price<2000'))
    bet_2000_3000 = len(df.query('home_price>=2000 & home_price<3000'))
    higher_3000 = len(df.query('home_price>=3000'))
    data = [['<1000', lower_1000], ["1000-2000", bet_1000_2000], ["2000-3000", bet_2000_3000], ['>=3000', higher_3000]]
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
            "",
            data,
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="租金统计情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    c.load_javascript()
    return c


data7 = diff_home_price_count(df)

# In[18]:


data7.render()


# In[19]:


# 面积统计情况：分为50㎡以下、 50㎡至80㎡ 、80㎡-100㎡ 和100㎡以上这几个部分
def diff_home_area_count(df):
    df = df.query('home_area != "未知"')
    lowwer_50 = len(df.query('home_area<50'))
    bet_50_80 = len(df.query('home_area>=50 & home_area<80'))
    bet_80_100 = len(df.query('home_area>=80 & home_area<100'))
    higher_100 = len(df.query('home_area>=100'))
    data = [['<50㎡', lowwer_50], ["50-80㎡", bet_50_80], ["80-100㎡", bet_80_100], ['>100㎡', higher_100]]
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
            "",
            data,
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="面积统计情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    c.load_javascript()
    return c


data8 = diff_home_area_count(df)

# ============ 可视化 ============

# In[20]:


data8.render("租金统计情况.html")


# ============ 分析 ============
# 

# 由上图可知，成都大多数出租房屋的每个月的租金都集中在2000元以上，这说明成都青年的租房压力还是比较大的。受到近年来成都房价迅速增长的影响以及随着人们消费水平的不断提升，成都的出租房的价格也呈现出较快增长。目前，成都租户每个月需要支出租金大多为2000元以上。

# ### 4.8 面积与价格的相关性分析

# ============ 代码 ============

# In[21]:


# 面积与价格的相关性分析
def relation_house(df):
    # 分割测试集和训练集
    x_train, x_test, y_train, y_test = train_test_split(df['home_area'], df['home_price'], test_size=0.25)
    # 进行标准化处理 实例化两个标注化API
    std_x = StandardScaler()

    x_train = std_x.fit_transform(x_train.values.reshape(-1, 1))
    x_test = std_x.transform(x_test.values.reshape(-1, 1))

    # 目标值 转换数组形状
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.values.reshape(-1, 1))
    y_test = std_y.transform(y_test.values.reshape(-1, 1))

    lr = LinearRegression()

    lr.fit(x_train, y_train)

    x_lr_test = std_x.inverse_transform(lr.predict(x_test))
    y_lr_test = std_y.inverse_transform(y_test)
    x = [int(i[0]) for i in x_lr_test.tolist()]
    y = [i[0] for i in y_lr_test.tolist()]
    c = (
        Scatter()
            .add_xaxis(x)
            .add_yaxis("价格", y, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="面积与价格的相关性分析"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        )
    )
    c.load_javascript();
    return c


data9 = relation_house(df)

# ============ 可视化 ============

# In[22]:


data9.render("面积与价格的相关性分析.html")

# ============ 分析 ============

# 由以上散点图可知，住房面积和房价呈现正向相关。整体而言，呈现出一种倾斜向上的直线趋势。这也符合我们的预期，一般而言，出租房屋的面积越大，相应的租金也自然越高。

# ## 5 总结

# 总体来看，成都的租房资源大多集中在市中心武侯区、高速发展区高新区和天府新区这三个区；出租房屋的户型大多是2室1厅、4室1厅、3室1厅这种一厅室的住房；出租房屋的面积过半数都是在80㎡以下，以小面积的租房为主；出租房屋的楼层分布较为均匀，没有明显的差异；大多数的出租房屋所在楼都安装了电梯；大多数的出租房屋的住房朝向都是坐北朝南；出租房屋的租金价格大多都集中在2000元以上；出租房屋的面积和租金整体而言呈现出一种正向相关的关系，即出租房屋的面积越大，租金越高。
