# from urllib.request import Request, urlopen

# url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=1"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# request = Request(url, headers=headers)
# try:
#     response = urlopen(request)
#     print(response.read().decode('utf-8')[:1000])  # Print the first 1000 characters of the response
# except Exception as e:
#     print(e)

from urllib.request import Request, urlopen
import ssl
import certifi

url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

request = Request(url, headers=headers)
try:
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(request, context=context)
    print(response.read().decode('utf-8')[:1000])  # Print the first 1000 characters of the response
except Exception as e:
    print(e)