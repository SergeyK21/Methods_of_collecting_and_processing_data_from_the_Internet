import requests
import urllib3

# import wget
#
# url = ''
# wget.dounload(url)
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}
http = urllib3.PoolManager(headers=headers)
url = 'https://www.avito.ru/'
resp = http.request('GET', url)
print(resp.status)