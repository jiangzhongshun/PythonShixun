from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def maoyan():
    def spider():
        driver = webdriver.Chrome()
        driver.get('https://maoyan.com/board/4')

        get_data(driver)
        pass

    def get_data(driver):
        datas = driver.find_elements_by_css_selector('dd')
        # print(datas)

        for data in datas:
            # 获取电影的名字
            # data_name = data.find_element_by_tag_name('a').get_attribute('href')
            data_name = data.find_element_by_tag_name('a').get_attribute('title')

            # 获取主演
            data_actor = data.find_element_by_class_name('star').text

            # 获取时间
            data_time = data.find_element_by_class_name('releasetime').text

            # 获取评论
            data_score = data.find_element_by_class_name('score').text

            # 规范获取信息的格式，字符串格式化
            msg = '''
                电影名:%s
                :%s
                :%s
                评分:%s
            ''' % (data_name, data_actor, data_time, data_score)
            movies.objects.create(movieName=data_name, movieActor=data_actor, movieTime=data_time,
                                  movieGrade=data_score)
            # with open(file='TOP100榜单', mode='a', encoding='utf-8') as f:
            #     f.write(msg)
            #     f.close()

        # 抓取大量数据
        button = driver.find_element_by_partial_link_text("下一页")

        # 点击加载
        button.click()
        # 加载网页时间
        time.sleep(1)

        # 再次调上面函数，起到循环作用
        get_data(driver)
        pass

    spider()