# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class Xiachufang2Spider(scrapy.Spider):
	name = 'xiachufang2'
	allowed_domains = ['xiachufang.com']
	start_urls = ['https://www.xiachufang.com/category/']
	# 自定义配置，换ip
	custom_settings = {
		"DOWNLOADER_MIDDLEWARES": {
			'spider.middlewares.SpiderDownloaderMiddleware': 543,
		}
	}

	def parse(self, response):
		div_list = response.xpath('//div[@class="block-bg p40 font16"]/div')
		for div in div_list:
			item = {}
			item["b_cate"] = div.xpath('.//h3[1]/text()').extract_first()
			h4_list = div.xpath('./div[@class="cates-list-all clearfix hidden"]/h4')
			for h4 in h4_list:
				item["m_cate"] = [m.strip() for m in h4.xpath(".//text()").extract() if m.strip() != ""][0]
				li_list = h4.xpath('./following-sibling::ul[1]/li')
				for li in li_list:
					item["s_cate"] = li.xpath('./a/text()').extract_first()
					item["s_href"] = response.urljoin(li.xpath('./a/@href').extract_first())
					# print("%s-%s-%s" % (item["b_cate"], item["m_cate"], item["s_cate"]))
					yield scrapy.Request(
							item["s_href"],
							callback=self.parse_list,
							meta={"item": deepcopy(item)}
					)
					return

	def parse_list(self, response):
		li_list = response.xpath(
			'//div[@class="pure-u-3-4 category-recipe-list"]/div[@class="normal-recipe-list"]/ul/li')
		for li in li_list:
			item = deepcopy(response.meta["item"])
			item["name"] = li.xpath('.//p[@class="name"]/a/text()').extract_first().strip()
			item["href"] = response.urljoin(li.xpath('.//p[@class="name"]/a/@href').extract_first())
			# print(item)
			yield scrapy.Request(
					item["href"],
					callback=self.parse_detail,
					meta={"item": item}
			)

	# next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
	# if next_url is not None:
	# 	next_url = response.urljoin(next_url)
	# 	yield scrapy.Request(
	# 		next_url,
	# 		callback=self.parse_list,
	# 		meta={"item": response.meta["item"]}
	# 	)

	def parse_detail(self, response):
		item = response.meta["item"]
		item["img"] = response.xpath('//img[@itemprop="image"]/@src').extract_first()
		item["pingfen"] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
		item["renshu"] = response.xpath(
			'//div[@class="cooked float-left"]/span[@class="number"]/text()').extract_first()
		item["desc"] = [c.strip() for c in response.xpath('//div[@itemprop="description"]/text()').extract()]

		item["ings"] = []
		tr_list = response.xpath('//tr[@itemprop="recipeIngredient"]')
		for tr in tr_list:
			ing = {}
			ing["name"] = tr.xpath('./td[1]/a/text()').extract_first().strip()
			ing["unit"] = tr.xpath('./td[2]/text()').extract_first().strip()
			item["ings"].append(ing)

		item["steps"] = []
		li_list = response.xpath('//div[@class="steps"]/ol/li')
		for li in li_list:
			step = {}
			step["content"] = li.xpath('./p/text()').extract_first()
			step["img"] = li.xpath('./img/@src').extract_first()
			item["steps"].append(step)

		item["tip"] = response.xpath('//div[@class="tip"]/text()').extract()

		print(item)
