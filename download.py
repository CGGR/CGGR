import requests, os, json, UnityPy, shutil, sys
from datetime import datetime
import cggr

sys.stderr = open('err.log', 'w')

whitelist = ("codelink/illust1024/", "character/background/", "character/messageface/", "character/illust2048/", "character/illustfull/")

with open("old.json", "r") as f:
	old = json.load(f)

cg = cggr.CGGR()

#Set Env
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as f:
    f.write("CRC=" + cg.GetCrc())

update = []
for filename in cg.fileList:
	try:
		if cg.fileList[filename] != old[filename]: #Updated file
			update.append(filename)
	except KeyError as e: #New file
		update.append(filename)

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
