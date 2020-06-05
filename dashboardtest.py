from PIL import Image,ImageDraw,ImageFont
import requests


newsUrl = "https://newsapi.org/v2/top-headlines?" 
newsUrl += "sources=bbc-news"
newsUrl += "&apiKey=72d48922d4644d03bcda247a8ba59479"

weatherUrl = "http://api.openweathermap.org/data/2.5/weather?"
weatherUrl += "q=Deal"
weatherUrl += "&appid=b1fef35e73e92d824c8b42ea70b5e913"

articles = []

response = requests.get(newsUrl)
print("got news")
newsData = response.json()

for article in newsData['articles']:
    articles.append(article['description'])


response = requests.get(weatherUrl)
print("got weather")
weatherData = response.json()
weatherStr = "Weather in Deal : " + weatherData['weather'][0]['main']
print(weatherData['weather'][0]['main'])


timeFont = ImageFont.truetype('Bellota-Regular.ttf', 22)
weatherFont = ImageFont.truetype('OpenSans-Regular.ttf', 16)
newsFont = ImageFont.truetype('OpenSans-Regular.ttf', 14)

time_image = Image.new('1', (250, 122), 255)
time_draw = ImageDraw.Draw(time_image)

# print(newsFont.getsize(articles)[0])

time_draw.text((10, 10), "dateTimeInfo", font = timeFont, fill = 0)

time_draw.text((20, 50), weatherStr, font = weatherFont, fill = 0)

time_draw.rectangle(((0, 100), (250, 122)), fill = 0)
time_draw.text((10, 100), articles[0], font = newsFont, fill = 255)

time_image.show()


