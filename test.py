import redis
import requests


file = open('image.jpg', 'rb')
data = {'size': '{"height": "150", "width": "50"}'}

r = requests.post('http://localhost:5000/resizer/load', files=dict(file=file), data=data)
print(r.text)

#r = requests.post('http://localhost:5000/api/get', json={'id': '2'})
#print(r.text)

#r = requests.post('http://localhost:5000/api/new', json={'text': 'ill fuck your mom'})

'''
curl -i -H "Content-Type: application/json" -X POST -d '{\'id\': \'2\'}'http://localhost:5000/api/get

'''