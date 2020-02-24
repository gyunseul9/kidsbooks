# -*- coding: utf-8 -*- 

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
import sys
from mod_books import Utilities,Tag
from config import Configuration
from db import DBConnection,Query
import codecs
import urllib.request


class Books:

	def __init__(self,ranking,platform):
		#print('init')
		self.ranking = ranking
		self.platform = platform

	def set_params(self):
		#print('set_params')
		self.ranking = sys.argv[1]
		self.platform = sys.argv[2]

	def validate(self):
		#print('validate')
		default	= {
			'ranking':'1',
			'platform':'local'
		}

		self.ranking = default.get('ranking')	if self.ranking == '' else self.ranking
		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()				

	def crawling(self):

		#print('crawling')
		self.validate()

		try:
			
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			now = time.localtime()			
	
			main = 'https://book.naver.com/bestsell/bestseller_list.nhn?cp=yes24&cate=001001027'				

			options = webdriver.ChromeOptions()
			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')
			options.add_argument('disable-gpu')
			options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
			options.add_argument('lang=ko_KR')
			options.add_argument('--log-level=3')
			
			driver = webdriver.Chrome('/Users/lonbehold/Bitbucket/kidsbooks/chromedriver', chrome_options=options)
			driver.implicitly_wait(3)
			driver.get('about:blank')
			driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
			driver.get(main)

			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			src = '네이버 책'

			update = Tag.mainpage(soup,'update',self.ranking)
			array = Tag.mainpage(soup,'array',self.ranking)
			link = Tag.mainpage(soup,'link',self.ranking)
			bid = Tag.mainpage(soup,'bid',self.ranking)
			thumbnail = Tag.mainpage(soup,'thumbnail',self.ranking)
			title = Tag.mainpage(soup,'title',self.ranking)
			author = Tag.mainpage(soup,'author',self.ranking)
			publisher = Tag.mainpage(soup,'publisher',self.ranking)
			date = Tag.mainpage(soup,'date',self.ranking)
			summary = Tag.mainpage(soup,'summary',self.ranking)

			print('출처: ',src)
			print('게시번호 :',bid)
			print('업데이트 : ',update)
			print('순위: ',self.ranking,'/',array)
			print('상세보기: ',link)
			print('책표지: ',thumbnail)
			print('책제목: ',title)
			print('저자: ',author)
			print('출판사: ',publisher)
			print('출판일: ',date)
			print('요약: ',summary)								

			cnt = conn.exec_select_books(bid,update)

			print('cnt:',cnt)

			if cnt:
				print('overlap seq: ',cnt)
			else:	
				print('does not overlap seq: ',cnt)
				conn.exec_insert_books(src,bid,update,self.ranking,link,thumbnail,title,author,publisher,'','',summary,date)

		except Exception as e:
			with open('./kidsbooks.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	books = Books('','')
	books.set_params()
	books.crawling()

if __name__ == "__main__":
	run()
