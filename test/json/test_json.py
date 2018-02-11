# coding = utf-8
import json

fi=open("test.jsn")
text = fi.read()
fi.close()
print (text)

obj = json.loads(text)
load_proxies = obj["RESULT"]
for proxy in load_proxies:
    print(proxy["ip"]+":"+proxy["port"])
