'''
    2017.11.16
    get_news.py : Get news list/contents from http://www.matsu.gov.tw/chhtml/news/371030000A/25
    新聞櫥窗 http://www.matsu.gov.tw/chhtml/news/371030000A/25
    公告事項 http://www.matsu.gov.tw/chhtml/news/371030000A/26
    年度活動 http://www.matsu.gov.tw/chhtml/newslist/371030000A/27
    徵求人才 http://www.matsu.gov.tw/chhtml/news/371030000A/29
    語音專區 http://www.matsu.gov.tw/chhtml/medialist/371030000A/30

    各局處檔案下載 http://www.matsu.gov.tw/chhtml/download/371030000A/43
    細說馬祖 > 生態環境 http://www.matsu.gov.tw/chhtml/newslist/371030000A/580
    細說馬祖 > 文化風情 http://www.matsu.gov.tw/chhtml/newslist/371030000A/600
    縣內景緻 > 鄉鎮特產 http://www.matsu.gov.tw/chhtml/specialtylist/371030000A/51
    縣內景緻 > 景點導覽 http://www.matsu.gov.tw/chhtml/landscapelist/371030000A/52

    資訊公開 > 業務統計 http://www.matsu.gov.tw/chhtml/downloadclass/371030000A/610


'''

import json
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
from time import sleep

baseURL = '..\\Data\\'
nodeURL = 'http://www.matsu.gov.tw/Chhtml/news/371030000A/25/?pagenum='

newsList = []

for i in range(1, 361) :
    reqURL = nodeURL + str(i)
    r = requests.get(reqURL)
    r = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

    # Get News List :
    contentList = r.find('div', class_ = 'FROM')

    listTemp = {}

    # Get News links = unique_ID
    idTemp = []
    urlTemp = []
    for j in contentList.find_all('a', class_ = 'LINK03') :
        searchURL = re.search('mcid=(.*)\"', str(j))
        if searchURL :
            linkID = searchURL.group().split(' ')[0][5:-1]
            linkURL = "http://www.matsu.gov.tw/chhtml/Detail/371030000A/25?mcid=" + linkID
            idTemp.append(linkID)
            urlTemp.append(linkURL)

    # get 日期/FIRST list
    dateTemp = []
    dateList = contentList.find_all('li', class_ = 'FIRST')
    for j in dateList :
        if '日期' not in j.get_text() :
            dateTemp.append(j.get_text())

    # get 標題/SECOND02 list
    titleTemp = []
    titleList = contentList.find_all('li', class_ = 'SECOND02')
    for j in titleList :
        if '標題' not in j.get_text() :
            titleTemp.append(j.get_text())

    # get 發佈單位/THREE01 list
    orgTemp = []
    orgList = contentList.find_all('li', class_ = 'THREE01')
    for j in orgList :
        if '發布' not in j.get_text() :
            orgTemp.append(j.get_text())

    # create obj dict : id / url / date / title / org
    for j in range(0, len(idTemp)) :
        listTemp = {
            'id' : idTemp[j],
            'date': dateTemp[j],
            'title' : titleTemp[j],
            'org' : orgTemp[j],
            'url': urlTemp[j],
        }

        newsList.append(listTemp)
    print('page -----', i)
with open(baseURL + 'news_list.json', 'w', encoding='utf-8') as f :
    json.dump(newsList, f, ensure_ascii=False, indent=4)






