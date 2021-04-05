from django.shortcuts import render
from .models import user
from .models import movies
from .models import goods
from django.shortcuts import redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Create your views here.

# http://localhost:8000/login 是登陆网页
# http://localhost:8000/zhuce 是注册网页
# http://localhost:8000/userList 是用户管理模块
# http://localhost:8000/showDatas 是爬虫数据展示

def loginFun(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #user01=authenticate(username=username,password=password)
        datas=user.objects.all()
        for data in datas:
            flag1=username == data.username
            flag2=password == data.password
            flag=flag1 and flag2
            if(flag):
                return render(request,'useCrawlers.html',locals())
                # return redirect('/useCrawlers.html')

        msg = '用户名密码错误'
        return render(request,'login.html',locals())

    return render(request,'login.html')

#注册方法，将注册的账号密码存入数据库
def zhuceFun(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user.objects.create(username=username,password=password)
        return render(request,'zhuceSuccess.html',locals())
    return render(request,'zhuce.html',locals())

def Crawler(request):
    if request.method=='POST':
        url=request.POST.get('crawlerUrl')
        #flag1判断是否是猫眼TOP100网站
        flag1=url=='https://maoyan.com/board/4'
        #flag2判断是否是jd网站，默认爬的是显卡
        flag2=url=='https://www.jd.com/'
        if(flag1):
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
                    movies.objects.create(movieName=data_name,movieActor=data_actor,movieTime=data_time,movieGrade=data_score)
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
            return render(request,'right.html',locals())

            # return redirect('right.html')
        if(flag2):
            def spider():
                # 1.定义浏览器
                driver = webdriver.Chrome()

                # 2.输入京东网址
                driver.get('https://www.jd.com/')

                # 3.定位输入关键字的搜索框，通过id来选定 id ='key'
                input_tag = driver.find_element_by_id('key')

                # 模拟键盘输入，输入关键字
                input_tag.send_keys('显卡')

                # 点击确定，回车键
                input_tag.send_keys(Keys.ENTER)

                # 设置加载时间,目的让网页加载
                time.sleep(5)

                # 抓取数据
                get_goods(driver)
                pass

            def get_goods(driver):
                # 二。定位商品，抓取数据
                # 1.分析网页当前口罩的分页列表，所有口罩的商品都展现在<li>标签中，这些不同分类的口罩商品的<li>标签的属性class="gl-item"都是一样的，所以我们去定位商品，选class属性去定位

                goods = driver.find_elements_by_class_name('gl-item')  # 查找多个节点，返回是个列表
                # print(type(goods))
                # # # print(goods)

                # for循环取出商品：名字，价格，评论，商品的链接
                for good in goods:
                    # 获取商品的链接：链接在<a>标签的href属性只不过
                    good_link = good.find_element_by_tag_name('a').get_attribute('href')

                    # 获取商品名字：在<div class ='p-name'>下的<a>标签下的<em>标签中，但是会发现当前的商品名字分三段展示，所以运用replace函数用空白代替换行
                    good_name = good.find_element_by_css_selector('.p-name em').text.replace('\n', '')

                    # 获取价格：同上可得
                    good_price = good.find_element_by_css_selector('.p-price i').text

                    # 获取评论
                    good_commit = good.find_element_by_css_selector('.p-commit a').text

                    # 规范获取信息的格式，字符串格式化
                    msg = '''
                        商品:%s
                        链接:%s
                        价格:%s
                        评论:%s
                    ''' % (good_name, good_link, good_price, good_commit)
                    goods.objects.create(goodName=good_name,goodLink=good_link,goodPrice=good_price,goodGrade=good_commit)
                    # print(msg)
                    # with open(file='显卡', mode='a', encoding='utf-8') as f:
                    #     f.write(msg)
                    #     f.close()

                # 抓取大量数据
                button = driver.find_element_by_partial_link_text("下一页")

                # 点击加载
                button.click()
                # 加载网页时间
                time.sleep(1)

                # 再次调上面函数，起到循环作用
                get_goods(driver)
                pass

            spider()
            return render(request, 'right.html', locals())
        else:
            return render(request,'wrong.html',locals())

    return render(request,'crawlerUrl.html',locals())


#从数据库里取出猫眼TOP100
def MaoyanTop100(request):
    data=movies.objects.all()
    # for data in data:
    #     print(data.movieName,data.movieActor,data.movieTime,data.movieGrade)
    return render(request,'showDatas.html',context={'data':data})

def userList(request):
    data=user.objects.all()
    return render(request,'userList.html',context={'data':data})