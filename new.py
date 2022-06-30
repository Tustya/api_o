import sys
import requests
import json
import time
import zipfile
import csv
import os
import pymysql
from pymysql.cursors import DictCursor


dateFrom = "2021-04-17"
dateTo = "2022-04-16"

client_secret = "thLhhO-fIM0m4UfyyV-Ud40m2rH8R74XoOopcrWU-RkJuvyWbmoG-lnAWDLGvpACytp680fgidP1q6ud4A"
client_ID = "2463140-1649243252017@advertising.performance.ozon.ru"

token_url = "https://performance.ozon.ru/api/client/token"
campaigns_url = "https://performance.ozon.ru:443/api/client/campaign"
phrases_url = "https://performance.ozon.ru:443/api/client/statistics/phrases"
statistics_url = "https://performance.ozon.ru:443/api/client/statistics/"
report_url = "https://performance.ozon.ru:443/external/api/statistics/report"

def getHeaders():
    data = dict(client_id=client_ID, client_secret=client_secret, grant_type='client_credentials')
    res = requests.post(token_url, data=data)
    j = json.loads(res.text)
    access_token = j['access_token']
    token_type = j['token_type']
    return {'Host': 'performance.ozon.ru:443', 'Authorization': token_type + ' ' + access_token, 'Content-Type': 'application/json'}

def getCampaigns():
    res = requests.get(campaigns_url, headers=headers)
    j = json.loads(res.text)
    lst = []
    for s in j['list']:
        lst.append(s['id'])
    return lst

def getObjects():
    lst = []
    for camp in campaigns:
        res = requests.get(campaigns_url + '/' + camp + '/objects',  headers=headers)
        j = json.loads(res.text)
        if 'list' in j:
            for s in j['list']:
                if s['id'] not in lst:
                    lst.append(s['id'])
    return lst

def getUUID():
    data = json.dumps(dict(
        campaigns=campaigns,
        objects=objects,
        dateFrom=dateFrom,
        dateTo=dateTo,
        groupBy="DATE"
    ))
    res = requests.post(phrases_url, data=data, headers=headers)
    j = json.loads(res.text)
    if 'UUID' in j:
        print('Запущено формирование отчета, UUID '+j['UUID'])
        return j['UUID']
    else:
        print('Не удалось запустить формирование отчета, так как на сервере уже имеется активный процесс формирования отчета')
        sys.exit()

def getReport():
    answer = ''
    while answer == '':
        res = requests.get(report_url + '?UUID=' + UUID, headers=headers)
        if res.text != '{"error":"report not found"}':
            answer = res.content
        else:
            print('Ожидание окончания формирования отчета...')
            time.sleep(10)
    return answer

def csv2mysql(csvdata):
    print('Запись данных в БД...')
    with open('temp_csv.csv', 'w', encoding='utf-8') as csvfile:
        csvfile.write(csvdata)
    csvfile = open('temp_csv.csv', 'r', newline='', encoding='utf-8')
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    lst = []
    for row in csvreader:
        lst.append(row)
    if lst[1][0] == 'SKU':
        insert_query = "insert into t_phrases (sku, product_name, search_phrase, user_request, shows, clicks, ctr, consumption) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    else:
        insert_query = "insert into t_phrases (product_name, search_phrase, user_request, shows, clicks, ctr, consumption) values (%s, %s, %s, %s, %s, %s, %s)"

    ttt = []
    for i in range(2, len(lst)):
        t = tuple(lst[i])
        ttt.append(t)
        if (len(ttt) == 100) or (i == len(lst) - 1):
            cursor.executemany(insert_query, ttt)
            connection.commit()
            ttt = []
    csvfile.close()
    os.remove('temp_csv.csv')

connection = pymysql.connect(
        host='31.31.198.145',  # ip адрес сервера или localhost
        user='u1155422_notify',
        password='cw8kep!!',
        db='u1155422_dev',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
cursor = connection.cursor()

headers = getHeaders()
campaigns_all = getCampaigns()
campaigns = []
for i in range(len(campaigns_all)):
    campaigns.append(campaigns_all[i])
    if (len(campaigns) == 10) or (i == len(campaigns_all) - 1):
        objects = getObjects()
        UUID = getUUID()
        report = getReport()
        if len(campaigns) > 1:
            print('Получен массив файлов CSV')
            with open('archive.zip', 'wb') as f:
               f.write(report)
            zip = zipfile.ZipFile('archive.zip')
            csv_list = zip.namelist()
            for item in csv_list:
                txtdata = zip.read(item).decode('utf-8')
                print('Обработка файла '+item)
                csv2mysql(txtdata)
            zip.close()
            os.remove('archive.zip')
        else:
            print('Получен файл CSV')
            csv2mysql(report.decode('utf-8'))
        campaigns = []
connection.close()
print('Готово')