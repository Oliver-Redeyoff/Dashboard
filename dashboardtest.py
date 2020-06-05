from PIL import Image,ImageDraw,ImageFont
import requests


url = "https://newsapi.org/v2/top-headlines?" 
url += "sources=bbc-news"
url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

articles = ""

response = requests.get(url)
print("got news")
data = response.json()

for article in data['articles']:
    articles += "      " + article['description']


timeFont = ImageFont.truetype('Bellota-Regular.ttf', 22)
newsFont = ImageFont.truetype('OpenSans-Regular.ttf', 14)

time_image = Image.new('1', (250, 122), 255)
time_draw = ImageDraw.Draw(time_image)

print(newsFont.getsize(articles))

time_draw.text((10, 10), "dateTimeInfo", font = timeFont, fill = 0)
time_draw.text((-100, 50), articles, font = newsFont, fill = 0)

time_image.show()


