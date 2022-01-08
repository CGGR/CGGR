import requests, os, json, UnityPy, shutil
from datetime import datetime
import cggr

whitelist = ("codelink/illust1024/", "character/background/", "character/messageface/", "character/illust2048/", "character/illustfull/")

with open("old.json", "r") as f:
	old = json.load(f)

cg = cggr.CGGR()

#Set Env
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as f:
    f.write("CRC=" + cg.GetCrc())

update = (set(cg.fileList) - set(old))

cg.SaveFileList("old.json")

for filename in update:
	if filename.startswith(whitelist):
		bundlePath = cg.Download(filename) #Download bundle
		env = UnityPy.load(bundlePath)
		for path, obj in env.container.items():
			child = os.path.basename(path)
			if obj.type in ["Texture2D", "Sprite"]:
				data = obj.read()
				dest = os.path.dirname(bundlePath.replace("Bundles", "Assets"))
				os.makedirs(dest, exist_ok = True)
				img = data.image
				img.save(os.path.join(dest, child)) #Extract Image

#Make zip
zipfile = os.path.join("Archives", cg.GetCrc())
shutil.make_archive(zipfile, 'zip', "Assets")