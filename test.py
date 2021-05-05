#
# import urllib.request, json
# with urllib.request.urlopen("https://raw.githubusercontent.com/YassineBaghdadi/apps_alowing/main/hadefGazAbssManager.json") as url:
#     data = json.loads(url.read().decode())
#     print(data)

import base64
import requests

#
# url = 'https://api.github.com/repos/YassineBaghdadi/apps_alowing/contents/hadefGazAbssManager.json'
# req = requests.get(url)
#
# req = req.json()  # the response is a JSON
#     # req is now a dict with keys: name, encoding, url, size ...
#     # and content. But it is encoded with base64.
# # content = base64.decodestring(req)
# print(req)


#
# #todo replace texes for docx
from docx import Document
filename = input('the file > ')
old = input('old > ')
new = input('new > ')


doc = Document(filename)

def replace_text():
    for p in doc.paragraphs:
            if old in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if old in inline[i].text:
                        text = inline[i].text.replace(old, new)
                        inline[i].text = text

    doc.save(filename)
#todo end



replace_text()