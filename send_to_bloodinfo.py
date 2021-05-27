import requests
from bs4 import BeautifulSoup
import csv
import json
import datetime
import os

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
print(SLACK_WEBHOOK_URL)

today = str(datetime.datetime.today().date())
response = requests.get("https://www.bloodinfo.net/bloodstats_stocks.do")
html = response.text

soup = BeautifulSoup(html, 'html.parser')

oneStep = soup.select('.mb10')[0]

# 1일 소요량
전체소요량 = int(oneStep.select('tbody > tr')[0].select('td')[1].text.replace(',',''))
O소요량 = int(oneStep.select('tbody > tr')[0].select('td')[2].text.replace(',',''))
A소요량 = int(oneStep.select('tbody > tr')[0].select('td')[3].text.replace(',',''))
B소요량 = int(oneStep.select('tbody > tr')[0].select('td')[4].text.replace(',',''))
AB소요량 = int(oneStep.select('tbody > tr')[0].select('td')[5].text.replace(',',''))

# 현재 혈액보유량
전체혈액보유량 = int(oneStep.select('tbody > tr')[1].select('td')[1].text.replace(',',''))
O혈액보유량 = int(oneStep.select('tbody > tr')[1].select('td')[2].text.replace(',',''))
A혈액보유량 = int(oneStep.select('tbody > tr')[1].select('td')[3].text.replace(',',''))
B혈액보유량 = int(oneStep.select('tbody > tr')[1].select('td')[4].text.replace(',',''))
AB혈액보유량 = int(oneStep.select('tbody > tr')[1].select('td')[5].text.replace(',',''))

# 보유상태
전체보유상태 = oneStep.select('tbody > tr')[2].select('td')[1].text.replace(',','')
O보유상태 = oneStep.select('tbody > tr')[2].select('td')[2].text.replace(',','')
A보유상태 = oneStep.select('tbody > tr')[2].select('td')[3].text.replace(',','')
B보유상태 = oneStep.select('tbody > tr')[2].select('td')[4].text.replace(',','')
AB보유상태 = oneStep.select('tbody > tr')[2].select('td')[5].text.replace(',','')

print(전체소요량, B소요량, O소요량, A소요량, AB소요량)
print(전체혈액보유량, O혈액보유량, A혈액보유량, B혈액보유량, AB혈액보유량)
print(전체보유상태, O보유상태, A보유상태, B보유상태, AB보유상태)

final_data = f"var 전체소요량 = '{전체소요량}';\n\
var B소요량 = '{B소요량}';\n\
var O소요량 = '{O소요량}';\n\
var A소요량 = '{A소요량}';\n\
var AB소요량 = '{AB소요량}';\n\
var 전체혈액보유량 = '{전체혈액보유량}';\n\
var O혈액보유량 = '{O혈액보유량}';\n\
var A혈액보유량 = '{A혈액보유량}';\n\
var B혈액보유량 = '{B혈액보유량}';\n\
var AB혈액보유량 = '{AB혈액보유량}';\n\
var 전체보유상태 = '{전체보유상태}';\n\
var O보유상태 = '{O보유상태}';\n\
var A보유상태 = '{A보유상태}';\n\
var B보유상태 = '{B보유상태}';\n\
var AB보유상태 = '{AB보유상태}';\n\
"

with open('bloodinfo_data.js', "w", encoding="UTF-8-sig") as f_write:
    f_write.write(final_data)

l = [전체소요량, B소요량, O소요량, A소요량, AB소요량, 전체혈액보유량, O혈액보유량, A혈액보유량, B혈액보유량, AB혈액보유량, 전체보유상태, O보유상태, A보유상태, B보유상태, AB보유상태]
l
#######################
# send to slack
#######################
# Slack 인커밍 웹훅
slack_payload = {"text": f"*{today}* 오늘의 혈액정보입니다. :drop_of_blood: \n 1. 전체 소요량: {전체소요량} \n :o2:소요량 : {O소요량} \n :a:소요량 : {A소요량} \n :b:소요량 : {B소요량} \n :ab:소요량 : {AB소요량} \n \n 2. 전체혈액보유량 : {전체혈액보유량} \n :o2:혈액보유량 : {O혈액보유량} \n :a:혈액보유량 : {A혈액보유량} \n :b:혈액보유량 : {B혈액보유량} \n :ab:혈액보유량 : {AB혈액보유량} \n \n 3. 전체보유상태 : {전체보유상태} \n :o2:보유상태 : {O보유상태} \n :a:보유상태 : {A보유상태} \n :b:보유상태 : {B보유상태} \n :ab:보유상태 : {AB보유상태} \n ```*적정혈액보유량은 일평균 5일분이상입니다.*```"}
# 슬랙에 쏩니다!
req = requests.post(url=SLACK_WEBHOOK_URL, data=json.dumps(final_data))
print(req)
