# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class BaixingSpider(scrapy.Spider):
	name = 'baixing2'
	allowed_domains = ['baixing.com']
	# 进入首页会自动跳转到 郑州 然后选择招聘模块
	start_urls = ['http://zhengzhou.baixing.com/gongzuo/?src=topbar']
	# custom_settings = { # 自定义配置
	# 	"DOWNLOAD_DELAY": 10, # 下载延迟
	# }

	def parse(self, response):
		li_list = response.xpath('//ul[@class="hover-nav"]/li')
		for li in li_list:
			item = {}
			item["b_cate"] = li.xpath('./a[1]/text()').extract_first()
			dt_list = li.xpath('./dl/dt')
			for dt in dt_list:
				item["m_cate"] = dt.xpath('./a/text()').extract_first()

				# dd_list = dt.xpath('./following-sibling::*')
				# print(dd_list.xpath('./self::dd'))
				# return
				dd_list = dt.xpath('./following-sibling::*')
				for dd in dd_list:
					print(dd)
					if len(dd.xpath('./self::dd')) == 0:
						break
					item["s_cate"] = dd.xpath('./a/text()').extract_first()
					item["s_href"] = response.urljoin(dd.xpath('./a/@href').extract_first())
					yield scrapy.Request(
						item["s_href"],
						callback=self.parse_list,
						meta={"item": deepcopy(item)}
					)

	def parse_list(self, response):
		pass

