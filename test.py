#
# import urllib.request, json
# with urllib.request.urlopen("https://raw.githubusercontent.com/YassineBaghdadi/apps_alowing/main/hadefGazAbssManager.json") as url:
#     data = json.loads(url.read().decode())
#     print(data)

import base64
import requests


url = 'https://api.github.com/repos/YassineBaghdadi/apps_alowing/contents/hadefGazAbssManager.json'
req = requests.get(url)

req = req.json()  # the response is a JSON
    # req is now a dict with keys: name, encoding, url, size ...
    # and content. But it is encoded with base64.
# content = base64.decodestring(req)
print(req)
