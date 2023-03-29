import time
import json
from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
from flask import Flask
import os
import random
app = Flask(__name__)


li = []
searchPath = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B3%BC%ED%95%99%20%ED%8C%8C%EC%9D%B4%EC%8D%AC&sort=0&photo=0&field=0&pd=6&ds=2022.08.04&de=2023.01.31&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:6m,a:all&start="
pageCount = [i if i == 0 else i * 10 + 1 for i in range(21)]

for i in range(7):
    resp = requests.get(f'{searchPath}{pageCount[i]}')
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    totalNews= soup.select('div.news_area')

    for j in range(6):
        m = totalNews[j]
        url = m.select_one('a.news_tit')['href']
        title = m.select_one('a.news_tit').text
        message = m.select_one('div.dsc_wrap > a.api_txt_lines.dsc_txt_wrap').text
        date = m.select_one('span.info').text
        press = m.select_one('a.info.press').text
        dict_data = {"url": f"{url}","title": f"{title}", "message":f"{message}", "date":f"{date}","press":f"{press}"}
        json_data = json.dumps(dict_data)
        value = json.loads(json_data)
        li.append(value)

@app.route("/")
def index():
    return 'Hellow World'

@app.route("/api")
def api():
    return li[random.randint(0,len(li)-1)]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
