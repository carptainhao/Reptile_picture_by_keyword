#!/usr/bin/python
#-*- coding: utf-8 -*-

#*****************************
#****** 2018 3.14  ***********
#*****  Author: LQ  **********
#****** Python 3.6.3 *********
#**** 用于爬取百度的图片********
#*****************************
 
#*******本脚本运行时需要本机安装 Chrome 浏览器以及Chrome的驱动，同时需要selenium库的支撑********
from selenium import webdriver 
import time  
import urllib  
from bs4 import BeautifulSoup as bs
import re  
import os  
#****************************************************
base_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
base_url_part2='&oq=bagua&rsp=0'#base_url_part1以及base_url_part2都是固定不变的，无需更改
search_query='香港地铁站入口' #检索的关键词，可自行更改
location_driver='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'#Chrome驱动程序在电脑中的位置
 
class Crawler:
	def __init__(self):
		self.url=base_url_part1+search_query+base_url_part2
 
	#启动Chrome浏览器驱动
	def start_brower(self):
		# 启动Chrome浏览器  
		driver = webdriver.Chrome(location_driver)  
		# 最大化窗口，因为每一次爬取只能看到视窗内的图片
		driver.maximize_window()  
		# 浏览器打开爬取页面  
		driver.get(self.url)  
		return driver
 
	def downloadImg(self,driver):  
		t = time.localtime(time.time())
		foldername = str(t.__getattribute__("tm_year"))+"-"+str(t.__getattribute__("tm_mon"))+"-"+str(t.__getattribute__("tm_mday"))#定义文件夹的名字
		picpath = 'F:\\ZY\\subway\\xianggang\\%s' % (foldername)#下载到的本地目录 
		if not os.path.exists(picpath):   #路径不存在时创建一个  
			os.makedirs(picpath)
		# 记录下载过的图片地址，避免重复下载  
		img_url_dic = {} 
		x = 0  
		#当鼠标的位置小于最后的鼠标位置时,循环执行
		pos = 0     
		for i in range(2000):    #此处可自己设置爬取范围，本处设置为1，那么不会有下滑出现
			pos +=500 # 每次下滚500  
			js = "document.documentElement.scrollTop=%d" % pos    
			driver.execute_script(js)  
			time.sleep(2)
			#获取页面源码
			html_page=driver.page_source
			#利用Beautifulsoup4创建soup对象并进行页面解析
			soup=bs(html_page,"html.parser")
			#通过soup对象中的findAll函数图像信息提取
			imglist=soup.findAll('img',{'src':re.compile(r'https:.*\.(jpg|png)')})
			print(imglist)
			for imgurl in imglist:  
				if imgurl['src'] not in img_url_dic:
					target = picpath+'\\%s.jpg' % x  
					print ('Downloading image to location: ' + target + '\nurl=' + imgurl['src'])
					img_url_dic[imgurl['src']] = '' 
					urllib.urlretrieve(imgurl['src'], target) 
                    #urllib.urlopen(imgurl['src'], target)  
					x += 1  
					
	def run(self):
		print ('''      ************************************* 
		**      Welcome to use Spider      ** 
		*************************************''')  
		driver=self.start_brower()
		self.downloadImg(driver)
		driver.close()
		print ("Download has finished.")
 
if __name__ == '__main__':  
	craw = Crawler() 
	craw.run()






