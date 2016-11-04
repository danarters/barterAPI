from models import User

from argon2 import PasswordHasher

def checkHash(unhashed, hashed):
	try:
		PasswordHasher(time_cost=3).verify(hashed, unhashed)	
		return True
	except:
		return False

def hash(string):
	return PasswordHasher(time_cost=3).hash(string)

def verify(userId, authToken):
	user = User.objects.get(userId=userId).toDict()
	if checkHash(
		unhashed=userId+user['password'],
		hashed=authToken):
		return user
	else:
		return None

def getToken(user):
	return hash(str(user['userId'])+user.pop('password'))

def login(username, password):
	user = User.objects.get(username=username).toDict()
	if checkHash(password, user['password']):
		user['authToken'] = getToken(user)
		return user 
