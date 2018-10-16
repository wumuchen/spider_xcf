import requests
import json

class ProxyTest:
	def __init__(self):
		self.test_url = "http://pv.sohu.com/cityjson?ie=utf-8"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",}

	def get_ip_list(self):
		ip_list = []
		with open("proxy.json", "r", encoding="utf-8") as f:
			for line in f:
				ip_list.append(json.loads(line))
		return ip_list

	def parse_url(self, url, proxies, timeout=3):
		return requests.get(url, headers=self.headers, proxies=proxies, timeout=timeout).content.decode()

	def get_content_list(self, html_str):
		print(html_str)
		try:
			return json.loads(html_str[19:-1])
		except:
			return None

	def save_content_list(self, proxy_url):
		with open("proxy_ok.json", "w+", encoding="utf-8") as f:
			f.write(proxy_url + "\n")

	def run(self):
		ip_list = self.get_ip_list()
		for ip in ip_list:
			proxy_url = "http://%s:%s" % (ip["ip"], ip["port"])
			print(proxy_url)
			try:
				html_str = self.parse_url(self.test_url, proxies={"http": proxy_url}, timeout=3)
			except:
				print("%s timeout" % proxy_url)
				continue
			
			json_dict = self.get_content_list(html_str)
			if json_dict is not None and json_dict["cip"] == ip["ip"]:
				print("%s success" % proxy_url)
				self.save_content_list(proxy_url)
			else:
				print("%s fail" % proxy_url)

if __name__ == '__main__':
	spider = ProxyTest()
	spider.run()
