import csv
import json
import requests
import time
import pandas as pd
import pprint
import data

AllReport_url = 'https://api-seller.ozon.ru/v1/report/list'
url = 'https://api-seller.ozon.ru/v1/report/stock/create'
reportURL = 'https://api-seller.ozon.ru/v1/report/info'

headers = {'client-id': data.clientId, 'api-key': data.ApiKey}

# Получаем код для скачивания файла
r = requests.post(url, headers=headers).text
j = json.loads(r)
code = j['result']

# Получаем и читаем файл с данными
res = requests.post(reportURL, json=code, headers=headers).text
time.sleep(5)
j_csv = json.loads(res)
file_url = j_csv['result']['file']
# Проверка на наличие ссылки для скачивания файла с отчетом
if file_url != None:
        print('Ссылка есть, можно скачивать')
        csv_get = requests.get(file_url, headers=headers)
        #  Сохранение данных в csv
        with open('Reports/stock_report.csv', 'wb') as file:
                file.write(csv_get.content)
else:
        print('ссылки нет')
        time.sleep(5)
        data = {"page": 0, "page_size": 1000, "report_type": "ALL"}
        r = requests.post(url, json=data, headers=headers).text
        j = json.loads(r)
        last_file = j['result']['reports'][-1]['file']
        csv_get = requests.get(last_file, headers=headers)
        #  Сохранение данных в csv
        with open('Reports/stock_report.csv', 'wb') as file:
                file.write(csv_get.content)




# # Вывод таблицы в терминале с помощью pandas
# result = pd.read_csv('report.csv', delimiter=';', )
# print(result)
# # ПРоверка для комита