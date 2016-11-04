import requests
import time

baseUrl = 'http://127.0.0.1'
users = {'1': {}, '2': {}, '3': {}}
compare = lambda one, other: all([one[key] for key in other])

"""Get first user to test with"""
data = {'username': 'dan', 'password': 'password'}
users['1']['user'] = requests.post(baseUrl+'/signup', json=data).json()
if not users['1']['user']:
	users['1']['user'] = requests.put(baseUrl+'/login', json=data).json()
users['1']['headers'] = {'userId': users['1']['user']['userId'], 'authToken': users['1']['user']['authToken']}
print users

"""Make get calls with first user"""
url = baseUrl + '/user/' + users['1']['user']['userId']
testUser = requests.get(url, headers=users['1']['headers']).json()
print testUser
if not compare(users['1']['user'], testUser):
	raise BaseException 

"""Make an item"""
try:
	url = baseUrl + '/create-item'
	users['1']['item'] = requests.post(url, headers=users['1']['headers']).json()
except:
	print 'item request rejected'

"""Request for the item"""
url = baseUrl + '/user-item/' + users['1']['user']['userId']
testItem = requests.get(url, headers=users['1']['headers']).json()
print testItem

""""""

