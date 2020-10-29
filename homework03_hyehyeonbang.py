import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for tr in trs:
    num_tag = tr.select_one('td.number')

    # if num_tag is None:
    #     continue

    num = num_tag.text[0:2].strip()

    title_tag = tr.select_one('td.info > a.title.ellipsis')
    # if title_tag is None:
    #     continue

    title = title_tag.text.strip()

    singer_tag = tr.select_one('td.info > a.artist.ellipsis')
    # if singer_tag is None:
    #     continue

    singer = singer_tag.text
    print(int(num), title, singer)

    data = {
        'num': num,
        'title': title,
        'singer': singer,
    }

    db.music.insert_one(data)