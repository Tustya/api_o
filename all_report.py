import json
import requests
import pprint

url = 'https://api-seller.ozon.ru/v1/report/list'
reportURL = 'https://api-seller.ozon.ru/v1/report/info'

headers = {'client-id': '103883', 'api-key': '12fc9ece-0332-40b8-8af1-f51b9da46978'}

data = {"page": 0,
        "page_size": 1000,
        "report_type": "ALL"
}

r = requests.post(url, json=data, headers=headers).text
j = json.loads(r)
pprint.pprint(j)