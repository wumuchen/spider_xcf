import requests
import json
from lxml import etree

# 同步验证代理ip是否可用
class ProxyFetch:
	def __init__(self):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
			# "Referer": "http://www.xicidaili.com/",
		}

	def start_urls(self):
		return ["http://www.xicidaili.com/nn/%d" % i for i in range(1,2)]

	def parse_url(self, url):
		return requests.get(url, headers=self.headers).content.decode()

	def get_content_list(self, html_str):
		content_list = []
		html = etree.HTML(html_str)
		tr_list = html.xpath('//table[@id="ip_list"]/tr')[1:]
		for tr in tr_list:
			item = {}
			item["ip"] = tr.xpath('./td[2]/text()')[0]
			item["port"] = tr.xpath('./td[3]/text()')[0]
			content_list.append(item)
		return content_list

	def save_content_list(self, content_list):
		with open("proxy.json", "a+", encoding="utf-8") as f:
			for ip in content_list:
				f.write(json.dumps(ip))
				f.write("\n")

	def run(self):
		start_urls = self.start_urls()
		for url in start_urls:
			html_str = self.parse_url(url)
			# print(html_str)
			content_list = self.get_content_list(html_str)
			self.save_content_list(content_list)

if __name__ == '__main__':
	spider = ProxyFetch()
	spider.run()
