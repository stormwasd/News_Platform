import requests


url = 'http://175.24.172.64:5555/random'
print(requests.get(url).text)