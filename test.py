import requests
import json

url = "https://api-seller.ozon.ru" # Cсылку нужно поменять на боевую среду
method = "/v1/report/products/movement/create" # Сюда вбиваем нужный метод
print(url + method)
head = {
  "Client-Id": "103883", # сюда клиент id
  "Api-Key": "12fc9ece-0332-40b8-8af1-f51b9da46978" # Сюда Api-Key
}

# Сюда пишем параметры запроса
body = {"date_from": "2020-08-01T14:15:22Z",
        "date_to": "2021-08-01T14:15:22Z",
        "language": "DEFAULT"}
body = json.dumps(body) # Нужно передавать в озон именно так, потому что string он как json не понимает
response = requests.post(url + method, headers=head, data=body)

print(response.text) # ответ сервера Озон