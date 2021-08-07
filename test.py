import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE)
print(response.json())

input()

payload = {'value': 'value1', 'mode': 'value2', "replace_with": "null"}

r = requests.post(BASE, data=payload)
print(r.json())

input()

payload2 = {'value': 'value1', 'mode': 'value2', "wrong_key": "null"}

r = requests.post(BASE, data=payload2)
print(r.json())