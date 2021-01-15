import requests

try:
    r = requests.get('http://172.217.168.164')
except requests.exceptions.ConnectionError as e:
    print(e)