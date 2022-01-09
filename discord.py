import os, sys
from discord_webhook import DiscordWebhook, DiscordEmbed
from pprint import pprint
from datetime import datetime

webhookURL = sys.argv[1]
webhookURL2 = sys.argv[2]
crc = sys.argv[3]
releaseURL = sys.argv[4]

class MyWebhook:
	def __init__(self, url):
		self.filecount = 0
		self.webhook = DiscordWebhook(url=url, rate_limit_retry=True)
	def sendImg(self, filepath, filename):
		with open(filepath, "rb") as f:
			self.webhook.add_file(file=f.read(), filename=filename)
		#self.filecount += 1
		#if self.filecount == 10:
		response = self.webhook.execute(remove_embeds=True, remove_files=True)
		#self.filecount = 0
	def addEmbed(self, embed):
		self.webhook.add_embed(embed)
	def execute(self):
		response = self.webhook.execute(remove_embeds=True, remove_files=True)

webhook = MyWebhook(webhookURL)
webhook2 = MyWebhook(webhookURL2)

embed = DiscordEmbed(
	title="Game Update",
	description=crc,
	color='0x2F3136'
)
embed.set_footer(text=datetime.now().strftime("%d %b %Y"))
embed.set_url(releaseURL)


fileList = {
	"codelink/illust1024": {
		"name": "Card Files",
		"count": 0
	},
	"character/background": {
		"name": "Background Files",
		"count": 0
	},
	"character/messageface": {
		"name": "Face Files",
		"count": 0
	},
	"character/illust": {
		"name": "Illust Files",
		"count": 0
	}
}

#Count Files
for root, dirs, files in os.walk("Assets"):
	for filename in files:
		filepath = os.path.join(root, filename)
		webhook.sendImg(filepath, filename)
		webhook2.sendImg(filepath, filename)
		for i in fileList:
			if filepath.startswith(os.path.join("Assets", os.path.normpath(i))):
				fileList[i]["count"] += 1

for i in fileList:
	if fileList[i]["count"] > 0:
		embed.add_embed_field(name=fileList[i]["name"], value=fileList[i]["count"], inline=True)


webhook.addEmbed(embed)
webhook2.addEmbed(embed)
webhook.execute()
webhook2.execute()
