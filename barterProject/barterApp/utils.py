from models import * 
from django.http import JsonResponse
from datetime import datetime

def tradeItems(trade):
	if type(trade) is str:
		trade = Trade.objects.get(tradeId=tradeId).toDict()

	requestedItemOwner = Iten.objects.get(itemId=trade['requestedItem']).userId
	offeredItemOwner = Iten.objects.get(itemId=trade['offeredItem']).userId

	# swap post owners
	Iten.objects.filter(itemId__in=[trade['requestedItem'], trade['offeredItem']]).update(userId='', )
	Item.objects.filter(itemId=trade['requestedItem']).update(userId=offeredItemOwner, pendingRequests=0)
	Item.objects.filter(itemId=trade['offeredItem']).update(userId=requestedItemOwner, pendingRequests=0)
	
	# accept single trade
	Trade.objects.filter(tradeId=trade['tradeId']).update(accepted=True)

	# archive pending trades
	Trade.objects.filter(
		Q(requestedItem=trade['requestedItem'])|\
		Q(requestedItem=trade['offeredItem'])|\
		Q(offeredItem=trade['offeredItem'])|\
		Q(offeredItem=trade['requestedItem'])).update(pending=False)
	
	# archive timeline history
	Timeline.objects.filter(userId__in=[requestedItem, offeredItemOwner], end__isnull=True).update(end=datetime.utcnow)
	
	return True


