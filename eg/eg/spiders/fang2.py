# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy


class Fang2Spider(scrapy.Spider):
	name = 'fang2'
	allowed_domains = ['fang.com']
	start_urls = ['http://www.fang.com/SoufunFamily.htm']


	def parse(self, response):
		tr_list = response.xpath('//div[@id="c02"]/table/tr')[:-1]
		sheng = ""
		for tr in tr_list:
			item = {}
			item["sheng"] = tr.xpath('.//strong/text()').extract_first()

			if item["sheng"] is not None and item["sheng"].strip() != "":
				sheng = item["sheng"]
			else:
				item["sheng"] = sheng

			a_list = tr.xpath('./td[3]/a')
			for a in a_list:
				item["shi"] = a.xpath('./text()').extract_first()
				item["shi_href"] = a.xpath('./@href').extract_first()
				if item["shi_href"] == "http://bj.fang.com/":
					item["new_href"] = "http://newhouse.fang.com/house/s/"
				else:
					item["new_href"] = re.sub(r'http://([a-z\.]+)/?', r'http://newhouse.\1/house/s/', item["shi_href"])
				# print(item)
				print("%s-%s" % (item["sheng"], item["shi"]))
				# yield scrapy.Request(
				# 	item["new_href"],
				# 	callback=self.parse_list,
				# 	meta={"item": deepcopy(item)}
				# )

	def parse_list(self, response):
		li_list = response.xpath('.//div[@id="newhouse_loupai_list"]/ul/li')
		for li in li_list:
			if len(li.xpath('./div[@class="clearfix"]/h3')) > 0:
				continue
			item = deepcopy(response.meta["item"])
			item["name"] = li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first().strip()
			item["href"] = li.xpath('.//div[@class="nlcd_name"]/a/@href').extract_first()
			# print(item)
			yield scrapy.Request(
				item["href"],
				callback=self.parse_detail,
				meta={"item":item}
			)

		next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
		if next_url is not None:
			next_url = response.urljoin(next_url)
			yield scrapy.Request(
				next_url,
				callback=self.parse_list,
				meta={"item":response.meta["item"]}
			)

	def parse_detail(self, response):
		item = response.meta["item"]
		item["price"] = response.xpath('//span[@class="prib cn_ff"]/text()').extract_first().strip()
		yield item
