from bs4 import BeautifulSoup as Soup
import requests
import pymysql
import random

host = 'localhost'
user = 'root'
password = 'eHC%8FcXG'
database = 'myb'

# link = "https://www.who.int/news/item/11-01-2023-beyond-blaming-people--why-journalists-must-dig-into-the-causes-of-road-crashes"
link = input("Введите ссылку на статью: ")


response = requests.get(link)
soup = Soup(response.content, 'html.parser')
tags = soup.find_all(["h", "h1","h3","p"])
text = []

for string in tags:
	text.append(string.text)

text = "".join(text)
text = text.split("Subscribe to our newsletters")[0]


mydivs = soup.findAll(class_="background-image single-image")
for div in mydivs:
	imageLink = f'https://www.who.int{div["data-image"]}'

name = random.randint(1000,10000)
name = f"{str(name)}.jpg"
img = requests.get(imageLink)
img_file = open(name, 'wb+')
img_file.write(img.content)
img_file.close()

con=pymysql.connect(host=host,user=user,password=password,database=database)
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists text (string VARCHAR(100000), name VARCHAR(50))")
    con.commit()
    cur.execute(f"""INSERT text(string,name) VALUES ("{text},{name}")""")
    con.commit()
