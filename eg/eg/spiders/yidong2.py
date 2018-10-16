# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class Yidong2Spider(scrapy.Spider):
	name = 'yidong2'
	allowed_domains = ['10086.cn']
	start_urls = ['https://shop.10086.cn/list/134_371_371_0_0_0_0.html']

	def parse(self, response):
		li_list = response.xpath('//div[@class="globalBorder selectFilter marginBottom10 noLeftFilter"]//li')[1:]
		for li in li_list:
			item = {}
			item["city_name"] = li.xpath('./a/text()').extract_first()
			item["city_href"] = "https://shop.10086.cn/list/134_%s_1_0_0_0_0_0.html" % li.xpath('./a/@location').extract_first()
			# print(item)
			yield scrapy.Request(
				item["city_href"],
				callback=self.parse_list,
				meta={"item":item}
			)

		item = {}
		item["city_name"] = "郑州"
		item["city_href"] = response.url
		response.meta["item"] = item
		for request in self.parse_list(response):
			yield request

	def parse_list(self, response):
		tr_list = response.xpath('//div[@class="goodsList"]/div/div/table/tbody/tr')
		for tr in tr_list:
			item = deepcopy(response.meta["item"])
			item["number"] = tr.xpath('./td[1]/text()').extract_first()
			item["price"] = tr.xpath('./td[2]/text()').re_first(r'\d+')
			print(item)
			yield item

		next_url = response.xpath('//a[text()=">"]/@href').extract_first()
		if next_url is not None:
			next_url = response.urljoin(next_url)
			yield scrapy.Request(
				next_url,
				callback=self.parse_list,
				meta={"item":response.meta["item"]}
			)
