from models import User, Trade, Item, Timeline
import auth
import utils
from decorators import authenticate 

from rest_framework.decorators import api_view 
from django.db.models import Q, F
from django.http import JsonResponse
from datetime import datetime


@api_view(['PUT'])
def login(request):
	user = auth.login(**request.data)
	return JsonResponse(user, status=200 if user else 401, safe=False)

@api_view(['POST'])
def signup(request):
	try:
		user = User.objects.create(
			username=request.data['username'],
			password=auth.hash(request.data['password']))
	except:
		return JsonResponse(0, status=417, safe=False)
	user.save()
	user = user.toDict()
	user['authToken'] = auth.getToken(user)
	return JsonResponse(user, safe=False)

@api_view(['GET'])
@authenticate
def getUser(request, userId=None):
	return JsonResponse(User.objects.get(userId=userId).toDict(exclude=['password']), safe=False)
	
@api_view(['GET'])
@authenticate
def getUserItem(request, userId):
	userId = userId or request.user['userId']
	return JsonResponse(Item.objects.get(userId=userId).toDict(), safe=False)

@api_view(['POST'])
@authenticate
def item(request):
	try:
		item = Item.objects.create(
			userId=request.user['userId'], 
			**request.data)
		item.save()
		Timeline.objects.create(
			userId=request.user['userId'],
			itemId=item.itemId).save()
		return JsonResponse(item.toDict(), safe=False)
	except:
		return JsonResponse(0, status=417, safe=False)

@api_view(['GET'])
@authenticate
def getUserTransactions(request, userId):
	userId = userId or request.user['userId']
	if userId != request.user['userId']:
		return JsonResponse(0, status=401, safe=False)
	return JsonResponse(Timeline.objects.filter(userId=userId).values(), safe=False)

@api_view(['POST'])
@authenticate
def request(request, itemId):
	try:
		offeredItem = Item.objects.get(owner=request.user['userId']).itemId
	except:
		return JsonResponse(0, status=417, safe=False)
	if Trade.objects.filter(
		userId=request.user['userId'], 
		requestedItem=itemId, 
		offeredItem=offeredItem, 
		pending=True):
		return JsonResponse(0, status=400, safe=False)
	else:
		trade = Trade.objects.create(
			userId=request.user['userId'], 
			requestedItem=itemId, 
			offeredItem=offeredItem,
			pending=True,
			accepted=False)
		if 'immediate' is 'trade':
			trade.accepted = True
			trade.pending = False
		else:
			Item.objects.filter(itemId=itemId).update(pendingRequests=F('pendingRequests')+1)

		trade.save()
		return JsonResponse(trade.toDict(), safe=False)
		## check if trade happens immediately

@api_view(['PUT'])
@authenticate
def accept(request, tradeId):
	trade = Trade.objects.get(tradeId=tradeId).toDict()
	if trade['userId'] != request.user['userId'] or not trade['pending']:
		return 'big ol fuck you'
	response = utils.tradeItems(trade)
	return JsonResponse(bool(response), status=200 if response else 400, safe=False)

@api_view(['PUT'])
@authenticate
def decline(request, tradeId):
	trade = Trade.objects.get(tradeId=tradeId).toDict()
	userItem = Item.objects.get(userId=request.user['userId']).toDict()
	if trade['requestedItem'] == userItem:
		success = Trade.objects.filter(
			tradeId=tradeId, 
			requestedItem=userItem, 
			pending=False).update(pending=True)
		return JsonResponse(success, safe=False)
	return JsonResponse(0, safe=False)


@api_view(['GET'])
@authenticate
def items(request):
	return JsonResponse(list(Item.objects.all().values()), safe=False)
	












