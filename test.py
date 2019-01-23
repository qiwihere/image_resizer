import redis
import requests


file = 123#open('img.jpg', 'rb')
data = {'size': '{"height": "250", "width": "50"}'}

r = requests.post('http://localhost:5000/resizer/load', files=dict(file=file), data=data)
print(r.text)

#r = requests.post('http://localhost:5000/api/get', json={'id': '2'})
#print(r.text)

#r = requests.post('http://localhost:5000/api/new', json={'text': 'ill fuck your mom'})

