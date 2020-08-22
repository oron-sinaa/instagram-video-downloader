import requests

r=requests.get("https://www.instagram.com/stories/blacchyna/2346056243183701129/", headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
test = r.text
print(test)