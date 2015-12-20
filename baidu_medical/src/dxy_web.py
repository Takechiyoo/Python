# -*- coding: utf-8 -*-
import scrapy
import re
from tutorial.items import TestItem
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

class TestSpider(scrapy.Spider):
	name = 'test_web'
	allow_domains = ['dxy.cn']
	start_urls = [
		'http://www.dxy.cn/',
		#'https://auth.dxy.cn/accounts/login?service=http%3A%2F%2Fwww.dxy.cn%2Fbbs%2Fboard%2F210%2F2069'
	]

	download_delay = 2
	post_information = {}
	next_page = 9

	def login(username,password):
		browser = webdriver.Firefox()
		wait = ui.WebDriverWait(browser,10)
 		
 		browser.get("https://auth.dxy.cn/accounts/login?service=http://www.dxy.cn/bbs/index.html")

 		user = browser.find_element_by_xpath('//input[@id="username"]')
 		user.send_keys(username, Keys.ARROW_DOWN)

 		passwd = browser.find_element_by_xpath('//input[@type="password"]')
 		passwd.send_keys(password, Keys.ARROW_DOWN)

 		vcode = browser.find_element_by_xpath('//input[@name="validateCode"]')
 		if vcode:
 			code = raw_input("verify code:")
 			if code:
 				vcode.send_keys(code, Keys.ARROW_DOWN)
 		browser.find_element_by_xpath('//button[@class="button"]').click()
 		ret = browser.get_cookies()
 		return ret


	def parse(self, response, my_cookies = login("15667083218", "abc@12345678")):
		for page in range(1, 2):
			url = 'http://www.dxy.cn/bbs/board/210/2069?tpg=' + str(page)
			yield scrapy.Request(url, cookies = my_cookies, callback = self.parse_thread)
		#yield scrapy.Request('http://www.dxy.cn/bbs/board/210/2069?tpg=9', cookies = my_cookies, callback = self.parse_thread)

	def parse_thread(self, response):
		print response.url
		for logo in response.xpath('//div[@id="logo"]'):
			print logo.extract()

		for topic in response.xpath('//td[@class="news"]/a'):
			url = topic.xpath('@href').extract()[0]
			yield scrapy.Request(url, callback = self.parse_post)
			#break
		#base_url = 'http://www.dxy.cn/bbs/board/210/2069?tpg='
		#next_page = 9
		#if response.url == 'http://www.dxy.cn/bbs/board/210/2069':
		#	next_page = 2
		#else:
		#self.next_page = int(response.url[-1]) + 1
		#print next_page
		#nxt_url = base_url + str(int(response.url[-1]) + 1)
		#print nxt_url
		#yield scrapy.Request(nxt_url, callback = self.parse_thread)
		print "success"

	def parse_post(self, response):
		p = re.compile(r'<.*?>')
		filename = 'dxybbs/' + response.url.split('/')[-1] + '.txt'
		topic = response.xpath('//title')[0].extract().strip()
		with open(filename, 'w') as f:
			f.write('topic: ' + p.sub('', topic).encode('utf-8') + '\n')
			#f.write(str(len(response.xpath('//td[@class="postbody"]'))) + '\n')
			#f.write(response.body)
			#f.write(response.body)
			for post in response.xpath('//td[@class="postbody"]'):
				f.write("post:\n")
				message = post.extract()
				f.write(p.sub('', message).encode('utf-8').strip() + '\n')
		# If the post has multiple pages comment
		pages = response.xpath('//div[@class="next_h"]')
		if len(pages) > 0:
			yield scrapy.Request(pages[0].xpath('a/@href').extract()[0], callback = self.parse_post_page)

	def parse_post_page(self, response):
		p = re.compile(r'<.*?>')
		filename = 'dxybbs/' + response.url.replace('?', '/').split('/')[-2] + '.txt'
		with open(filename, 'a') as f:
			#f.write('topic: ' + p.sub('', topic) + '\n')
			for post in response.xpath('//td[@class="postbody"]'):
				f.write("post:\n")
				message = post.extract()
				f.write(p.sub('', message).encode('utf-8').strip() + '\n')
		pages = response.xpath('//div[@class="next_h"]')
		if len(pages) > 0:
			yield scrapy.Request(pages[0].xpath('a/@href').extract()[0], callback = self.parse_post_page)
				#if "quote quote-collapse" in post.extract():  #contain quote
				#	message = post.extract().replace(post.xpath('//div[@class="quote quote-collapse"]')[0].extract(), '')
				#	f.write("post:\n")
				#	f.write(p.sub('', message).encode('utf-8').strip() + '\n')
				#else:
				#	f.write("post:\n")
				#	message = post.extract()
				#	f.write(p.sub('', message).encode('utf-8').strip() + '\n')

