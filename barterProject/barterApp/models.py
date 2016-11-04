from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import uuid

class User(models.Model):
	userId = models.UUIDField(primary_key=True, default=uuid.uuid4) 
	username = models.TextField(unique=True)
	password = models.TextField()

	class Meta:
		db_table = 'users'

	def __unicode__(self):
		return self.username

	def toDict(self, fields=None, exclude=[]):
		e = lambda key: key in set(exclude + ['_state'])
		f = lambda key: key in set(fields) if fields else lambda key: True
		data = {}
		for key in self.__dict__.iterkeys():
			if f(key) and not e(key):
				data[key] = getattr(self, key)
		return data

class Item(models.Model):
	itemId = models.UUIDField(primary_key=True, default=uuid.uuid4) 
	userId = models.UUIDField(unique=True)
	title = models.TextField(default='Something')
	description = models.TextField(default='This may or may not be an eggplant')
	image = models.TextField(default='http://i2.kym-cdn.com/entries/icons/original/000/019/068/lgJCmtjW_400x400.jpeg')
	pendingRequests = models.IntegerField(default=0)

	class Meta:
		db_table = 'items'

	def __unicode__(self):
		return self.title

	def toDict(self, fields=None, exclude=[]):
		e = lambda key: key in set(exclude+['_state'])
		f = lambda key: key in set(fields) if fields else lambda key: True
		data = {}
		for key in self.__dict__.iterkeys():
			if f(key) and not e(key):
				data[key] = getattr(self, key)
		return data

class Trade(models.Model):
	tradeId = models.UUIDField(primary_key=True, default=uuid.uuid4)
	userId = models.UUIDField()
	message = models.TextField(default='I have a proposition for you good sir')
	offeredItem = models.UUIDField()
	requestedItem = models.UUIDField()
	pending = models.BooleanField(default=True)
	accepted = models.BooleanField(default=False)

	class Meta:
		db_table = 'trades'

	def __unicode__(self):
		return self.message

class Timeline(models.Model):
	timelineId = models.UUIDField(primary_key=True, default=uuid.uuid4)
	itemId = models.UUIDField()
	start = models.DateTimeField(default=datetime.utcnow)
	end = models.DateTimeField(blank=True, null=True)





