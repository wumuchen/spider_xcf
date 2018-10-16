# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class Hao123soft2Spider(scrapy.Spider):
	name = 'hao123soft2'
	allowed_domains = ['hao123.com']
	start_urls = ['http://soft.hao123.com/']

	def parse(self, response):
		li_list = response.xpath('//ul[@class="child-cat"]/li')[1:]
		for li in li_list:
			item = {}
			item["cate_name"] = li.xpath('./a/@title').extract_first()
			item["cate_href"] = li.xpath('./a/@href').extract_first()
			# print(item["cate_href"])
			yield scrapy.Request(
				item["cate_href"],
				callback=self.parse_list,
				meta={"item": item}
			)

	def parse_list(self, response):
		li_list = response.xpath('//ul[@class="main-list"]/li')
		for li in li_list:
			item = deepcopy(response.meta["item"])
			item["name"] = li.xpath('.//a[1]/@title').extract_first()
			item["href"] = response.urljoin(li.xpath('.//a[1]/@href').extract_first())
			item["icon"] = li.xpath('.//img[1]/@src').extract_first()
			print(item["href"])
			yield scrapy.Request(
				item["href"],
				callback=self.parse_detail,
				meta={"item": item}
			)

		next_url = response.xpath('//a[text()=" 下一页"]/@href').extract_first()
		if next_url is not None:
			next_url = response.urljoin(next_url)
			yield scrapy.Request(
				next_url,
				callback=self.parse_list,
				meta={"item": response.meta["item"]}
			)

	def parse_detail(self, response):
		item = response.meta["item"]
		item["pic"] = response.xpath('//div[@class="pic-item"]/img/@src').extract_first()
		item["desc"] = response.xpath('//span[@class="all-desc"]/text()').extract_first()
		item["download"] = response.xpath('//a[@class="dl-btn"]/@href').extract_first()
		item["size"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="大小："]/../text()').extract_first()
		item["version"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="版本："]/../text()').extract_first()
		item["update_date"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="更新："]/../text()').extract_first()
		item["os_bit"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="系统位数："]/../text()').extract_first()
		item["comment"] = "".join(response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="评论："]/..//text()').extract())
		item["language"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="语言："]/../text()').extract_first()
		item["auth"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="授权："]/../text()').extract_first()
		item["os"] = response.xpath('//ul[@class="soft-info-list"]//span[@class="t_title" and text()="适合系统："]/../text()').extract_first()
		item["img_list"] = [response.urljoin(url) for url in response.xpath('//ul[@class="soft-cont-img"]//img/@src').extract()]
		item["image_urls"] = [item["icon"], item["pic"]] + item["img_list"]
		yield item