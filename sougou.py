#!/usr/bin/python
#-*- coding: utf-8 -*-

from selenium import webdriver
import time
import urllib
 
# 爬取页面地址
base_url_part1 = 'http://pic.sogou.com/pics?query='
base_url_part2='&w=05002100&p=&_asf=pic.sogou.com&_ast=1544274332&sc=index&oq=sugg_history_word&ri=0&sourceid=sugg&sut=1437&sst0=1544274331934'#base_url_part1以及base_url_part2都是固定不变的，无需更改
search_query='地铁站A出入口' #检索的关键词，可自行更改
url=base_url_part1+search_query+base_url_part2
 
# 目标元素的xpath
xpath = '//div[@id="imgid"]/ul/li/a/img'
 
# 启动Firefox浏览器
location_driver='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'#Chrome驱动程序在电脑中的位置
driver = webdriver.Chrome(location_driver) 
#driver = webdriver.Firefox()
 
# 最大化窗口，因为每一次爬取只能看到视窗内的图片
driver.maximize_window()
 
# 记录下载过的图片地址，避免重复下载
img_url_dic = {}
 
# 浏览器打开爬取页面
driver.get(url)
 
# 模拟滚动窗口以浏览下载更多图片
pos = 0
m = 6000 # 图片编号
for i in range(3000):
	pos += i*500 # 每次下滚500
	js = "document.documentElement.scrollTop=%d" % pos
	driver.execute_script(js)
	time.sleep(1)   
	
	for element in driver.find_elements_by_xpath(xpath):
		img_url = element.get_attribute('src')
		# 保存图片到指定路径
		if img_url != None and not img_url_dic.has_key(img_url):
			img_url_dic[img_url] = ''
			m += 1
			ext = img_url.split('.')[-1]
			filename = str(m) + '.' + 'jpg'#ext
			#保存图片数据
			data = urllib.urlopen(img_url).read()
			f = open('./sougou/' + filename, 'wb')
			f.write(data)
			f.close()
print ("Download has finished.")            
                     
driver.close()