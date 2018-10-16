# coding=utf-8
import requests
import json
import threading
from queue import Queue
import datetime

# 多线程验证代理ip是否可用
class ProxyTest:
	def __init__(self):
		self.test_url = "http://pv.sohu.com/cityjson?ie=utf-8"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",}
		self.request_queue = Queue()

	def get_ip_list(self):
		with open("proxy.json", "r", encoding="utf-8") as f:
			for line in f:
				ip = json.loads(line)
				self.request_queue.put(ip)

	def request(self):
		while True:
			ip = self.request_queue.get()

			proxy_url = "http://%s:%s" % (ip["ip"], ip["port"])
			# print("parse_url: %s" % proxy_url)

			try:
				starttime = datetime.datetime.now()
				response = requests.get(self.test_url, headers=self.headers, proxies={"http": proxy_url}, timeout=10)
				endtime = datetime.datetime.now()
				use_time = endtime - starttime
			except:
				print("%s timeout" % proxy_url)
				self.request_queue.task_done()
				continue

			html_str = response.content.decode()

			try:
				data = json.loads(html_str[19:-1])
			except:
				print("%s fail, use time %d" % (proxy_url, use_time.seconds))
				self.request_queue.task_done()
				continue

			if data["cip"] == ip["ip"]:
				print("%s success, use time %d, %s" % (proxy_url, use_time.seconds, html_str))
				self.request_queue.task_done()
			else:
				print("%s invalid, use time %d" % (proxy_url, use_time.seconds))
				self.request_queue.task_done()

	def run(self):
		thread_list = []
		
		# 读取ip地址文件 并存储到队列中
		self.get_ip_list()

		# 遍历，发送请求，获取响应
		for i in range(20):
			t_parse = threading.Thread(target=self.request)
			thread_list.append(t_parse)
		
		for t in thread_list:
			t.setDaemon(True) #把子线程设置为守护线程，该线程不重要主线程结束，子线程结束
			t.start()

		
		self.request_queue.join() #让主线程等待阻塞，等待队列的任务完成之后再完成

		print("主线程结束")


if __name__ == '__main__':
	proxy = ProxyTest()
	proxy.run()