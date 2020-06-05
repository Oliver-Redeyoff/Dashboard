import requests
import json

url = "https://newsapi.org/v2/top-headlines?" 
url += "sources=bbc-news"
url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

articles = []

response = requests.get(url)
print("got data")
data = response.json()

for article in data['articles']:
    articles.append(article['description'])

print(articles)

