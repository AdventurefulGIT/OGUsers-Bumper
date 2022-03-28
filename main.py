import cloudscraper
import base64
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
		
		self.username, self.uid = self.get_user_authenticated()
		print(f"Account authenticated\nUsername: {self.username}\nUID: {self.uid}")

		self.start_bot()

	def get_thread_id(self, thread_url):
		r = self.session.request(
				method = "GET",
				url = thread_url
			)
		return re.search(r"newreply\.php\?tid=(\d+)", r.text).group(1)

	def get_post_key(self):
		r = self.session.request(
				method = "GET",
				url = "https://ogusers.com/misc.php?action=help&hid=33",
			)
		return re.search(r"my_post_key = \"(.+?)\";", r.text).group(1)

	def get_user_authenticated(self):
		try:
			r = self.session.request(
				method = "GET",
				url = "https://ogusers.com/,"
			)
			return (re.search(r"Profile of ([^<]+)", r.text).group(1), re.search(r"uid=(\d+)", r.text).group(1))
		except:
			print("Detected Cloudflare challenge version 2\nThis bot does not currently support it, please try again later.\nThe challenge version may change depending on time of day.")
			quit()

	def send_post(self, message, thread_url):
		r = self.session.request(
				method = "POST",
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
	print(base64.b64decode('PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQogIFdlbGNvbWUgdG8gQ2xvdWQncyBPR1VzZXJzIEF1dG8gQnVtcGVyCgogIEFueSBxdWVzdGlvbnM/IENvbnRhY3QgbWUgb24gT0dVc2VycwogIGh0dHBzOi8vb2d1c2Vycy5jb20vbWVtYmVyLnBocD9hY3Rpb249cHJvZmlsZSZ1aWQ9NTUxNDIKCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Cg==').decode())
	OGUsers()
