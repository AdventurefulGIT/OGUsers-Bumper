import cloudscraper
import random
import json
import time
import re

class OGUsers:
	def __init__(self):
		self.session = cloudscraper.create_scraper()
		self.session.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

		self.config = json.load(open('config.json'))
		self.session.cookies.set("ogusersmybbuser", self.config['mybbuser'], domain="ogusers.com")

		self.last_post = ""

		self.start_bot()

	def get_thread_id(self, thread_url):
		r = self.session.get(
				url = thread_url
			)
		return re.findall("newreply\.php\?tid=(\d+)", r.text)[0]

	def get_post_key(self):
		r = self.session.get(
				url = "https://ogusers.com/misc.php?action=help&hid=33",
			)
		return re.search("my_post_key = \"(.+?)\";", r.text).group(1)

	def send_post(self, message, thread_url):
		r = self.session.post(
				url = "https://ogusers.com/newreply.php?ajax=1",
				data = {
					'my_post_key':self.get_post_key(),
					'subject':'',
					'action':'do_newreply',
					'posthash':'',
					'quoted_ids':'',
					'lastpid': 0,
					'tid':self.get_thread_id(thread_url),
					'method':'quickreply',
					'message':' %s' % message
				}
			)
		return r.text

	def random_post(self):
		post = random.choice(self.config['settings']['content'])
		return post if not post == self.last_post else self.random_post()

	def start_bot(self):
		while True:
			for thread in self.config['settings']['threads']:
				if '~~' in thread:
					thread, message = thread.split('~~')
					print(self.send_post(message, thread))

				elif len(self.config['settings']['content']) > 1:
					print(self.send_post(self.random_post(), thread))

				else:
					print(self.send_post(self.config['settings']['content'][0], thread))

				time.sleep(10)

			print('Waiting cooldown before sending next post!')
			time.sleep(self.config['settings']['delay'])

if __name__ == "__main__":
	OGUsers()
