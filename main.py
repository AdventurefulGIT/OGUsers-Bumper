import cloudscraper
import base64
import json
import time
import re

class OGUsers:
	def __init__(self):
		self.session = cloudscraper.create_scraper()
		self.session.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
		self.config = json.load(open('config.json'))
		self.session.cookies.set("ogusersmybbuser", self.config['mybbuser'], domain="ogusers.com")
		self.notifications = []
		
		self.start_bot()


	def get_notifications(self):
		try:
			r = self.session.get(
				url = 'https://ogusers.com/alerts.php?action=modal'
			)
			
			regex = re.compile(r'id=\d+\" style=\"font-size:15px;\">\s+(.*)')
			return regex.findall(r.text)
		except:
			print("Detected Cloudflare challenge version 2\nThis bot does not currently support it, please try again later.\nThe challenge version may change depending on time of day.")
			quit()


	def get_messages(self):
		r = self.session.get(
			url = 'https://ogusers.com/private.php'
		)
		regex = re.compile(r'<span class=\"unreadcount\" style=\"position: absolute;\">(\d+)</span>\s*.*\s.*\s.*\s.*\">((?:(?!\">).)*?)<\/.*\s.*>(.*)<')
		return regex.findall(r.text)


	def send_notification(self, notification):
		f_notification = re.sub('<span .*">', '', notification.replace('</span>', '').replace('<b>', '').replace('</b>', ''))
		data = {
			"embeds": [
				{
					"title":f"{f_notification}",
					"color": int(self.config['settings']['hex_color_notification'], 16)
				}
			]
		}
		r = self.session.post(
			url = self.config['settings']['webhook_url'],
			json = data
		)
		self.notifications.append(notification)
	

	def send_message(self, notification):
		data = {
			"embeds": [
				{
					"title":f"{notification[1]}({notification[0]}): {notification[2]}",
					"color": int(self.config['settings']['hex_color_message'], 16)
				}
			]
		}
		r = self.session.post(
			url = self.config['settings']['webhook_url'],
			json = data
		)
		self.notifications.append(notification)


	def start_bot(self):
		for notification in self.get_notifications():
			self.notifications.append(notification)

		for message in self.get_messages():
			self.notifications.append(message)

		while True:
			for notification in self.get_notifications():
				if not notification in self.notifications:
					print(notification, notification in self.notifications)
					self.send_notification(notification)

			for message in self.get_messages():
				if not message in self.notifications:
					self.send_message(message)

			time.sleep(self.config['settings']['delay'])
			


if __name__ == '__main__':
	print(base64.b64decode('PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQogIFdlbGNvbWUgdG8gQ2xvdWQncyBPR1VzZXJzIE5vdGlmaWVyIEJvdAoKICBBbnkgcXVlc3Rpb25zPyBDb250YWN0IG1lIG9uIE9HVXNlcnMKICBodHRwczovL29ndXNlcnMuY29tL21lbWJlci5waHA/YWN0aW9uPXByb2ZpbGUmdWlkPTU1MTQyCgo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQ==').decode())
	OGUsers()
