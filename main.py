import json
import requests

url = 'https://api-seller.ozon.ru/v1/report/products/movement/create'
reportURL = 'https://api-seller.ozon.ru/v1/report/info'

headers = {'client-id': '103883', 'api-key': '12fc9ece-0332-40b8-8af1-f51b9da46978'}

data = {"date_from": "2020-06-01T14:15:22Z",
        "date_to": "2021-08-01T14:15:22Z",
        "language": "DEFAULT"}

r = requests.post(url, json=data, headers=headers).text
j = json.loads(r)
code = j['result']

res = requests.post(reportURL, json=code, headers=headers).text
j_csv = json.loads(res)
csv = j_csv['result']['file']
csv_get = requests.get(csv, headers=headers).text
print(csv_get)

