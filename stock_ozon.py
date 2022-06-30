import csv
import json
import requests
import time
import pandas as pd

url = 'https://api-seller.ozon.ru/v1/report/stock/create'
reportURL = 'https://api-seller.ozon.ru/v1/report/info'

headers = {'client-id': '103883', 'api-key': '12fc9ece-0332-40b8-8af1-f51b9da46978'}

# # Получаем код для скачивания файла
# r = requests.post(url, headers=headers).text
# j = json.loads(r)
# code = j['result']
#
# # Получаем и читаем файл с данными
# res = requests.post(reportURL, json=code, headers=headers).text
# time.sleep(20)
# j_csv = json.loads(res)
# print(j_csv)
# csv1 = j_csv['result']['file']
# print(csv1)
# file = 'https://api-seller.ozon.ru/v1/report/file/78/c6/78c60504e85bed34.csv'
# csv_get = requests.get(file, headers=headers)
#
#
# #  Сохранение данных в csv
# with open('report.csv', 'wb') as file:
#         file.write(csv_get.content)

# Вывод таблицы в терминале с помощью pandas
result = pd.read_csv('report.csv', delimiter=';', )