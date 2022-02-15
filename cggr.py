import requests, json, base64, os
from Cryptodome.Cipher import AES

class CGGR:
	def __init__(self):
		self.GetClientVersion()
		self.GetInfo()
		self.GetBundlesList()

	def GetClientVersion(self):
		r = requests.get("http://itunes.apple.com/lookup?bundleId=jp.co.hakuhododymp.game&country=jp")
		self.clientVersion = json.loads(r.text)["results"][0]["version"]

	def GetInfo(self):
		body = {
			"osType": 2,
			"userId": ""
		}
		body["clientVersion"] = self.clientVersion
		r = requests.post("https://api.cggr-game.jp/version_check.php", data=body)
		self.info = json.loads(r.text)
		self.assetbundleInfoUrl = self.info["assetbundleInfoUrl"].format("", "", self.info["assetbundleInfoCrc"])

	def GetCrc(self):
		return self.info["assetbundleInfoCrc"]

	def GetBundlesList(self):
		r = requests.get(self.assetbundleInfoUrl)
		aes = AES.new(bytes.fromhex("AD4F2E98C5A023DA578E6B85D786EAC8"), AES.MODE_CBC, bytes.fromhex("0123456789ABCDEF0123456789ABCDEF"))
		self.decode = aes.decrypt(base64.b64decode(r.content)).decode("utf-8")
		self.bundleList = json.loads(self.decode[:self.decode.rfind('}') + 1])
		self.GetFileList()

	def GetFileList(self):
		self.fileList = {}
		for item in self.bundleList["AssetBundles"]:
			self.fileList[item["name"]] = item["crc"]

	def SaveFileList(self, filename):
		with open(filename, "w") as f:
			f.write(json.dumps(self.fileList, indent=4))

	def Download(self, filename, parent = "Bundles"):
		r = requests.get(self.info["assetbundlePath"].format("", filename, self.fileList[filename]))
		filename = os.path.normpath(filename)
		os.makedirs(os.path.dirname(os.path.join(parent, filename + ".unity3d")), exist_ok = True)
		with open(os.path.join(parent, filename + ".unity3d"), "wb") as f:
			f.write(r.content)
		return os.path.join(parent, filename + ".unity3d")
