import requests
import random
import json
import time
import re


class OGUsers:
	def __init__(self):
		self.scraper = requests.Session()
		self.config = json.load(open('config.json'))
		self.cookies = {'ogusersmybbuser':self.config['mybbuser'], 'oguserssid':self.config['sid']}
		self.lastpost = ""

		self.startBot()

	def getTID(self, thread):
		r = self.scraper.get(thread, cookies=self.cookies)
		return re.findall("newreply\.php\?tid=(\d+)", r.text)[0]

	def getPostKey(self):
		url = "https://ogusers.com/misc.php?action=help&hid=6"
		try:
			r = self.scraper.get(url, cookies=self.cookies, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
			return re.search("my_post_key = \"(.+?)\";", r.text).group(1)
		except:
			print('Failed to get post key: ', e)
			pass

	def sendPost(self, message, thread_url):
		return self.scraper.post('https://ogusers.com/newreply.php?ajax=1', 
			data={
					'my_post_key':self.getPostKey(),
					'subject':'',
					'action':'do_newreply',
					'posthash':'',
					'quoted_ids':'',
					'lastpid': 0,
					'tid':self.getTID(thread_url),
					'method':'quickreply',
					'message':' ' + str(message)
				}, cookies=self.cookies).text

	def randomPost(self):
		x = random.choice(self.config['settings']['content'])
		return x if x != self.lastpost else randomPost()

	def startBot(self):
		while 1:
			for thread in self.config['settings']['threads']:
				if len(self.config['settings']['content']) > 1:
					print(self.sendPost(self.randomPost(), thread))
				else:
					print(self.sendPost(self.config['settings']['content'][0], thread))
				time.sleep(10)

			print('Waiting cooldown before sending next post!')
			time.sleep(self.config['settings']['delay'])


OGUsers()
