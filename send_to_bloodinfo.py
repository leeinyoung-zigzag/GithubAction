import requests
from bs4 import BeautifulSoup
import csv
import json

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
slack_incoming_url = "https://hooks.slack.com/services/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" # 수정5
slack_payload = final_data
# 슬랙에 쏩니다!
req = requests.post(url=slack_incoming_url, data=json.dumps(final_data))
print(req)
