from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
	url(r'^signup[\/]?$', views.signup),
	url(r'^login[\/]?$', views.login),

	url(r'^create-item[\/]?$', views.item),

	url(r'^user[\/]?(?P<userId>[0-9a-f\-]{36})?[\/]?$', views.getUser),
	url(r'^user-item[\/]?(?P<userId>[0-9a-f\-]{36})?[\/]?$', views.getUserItem),
	url(r'^user-transactions[\/]?(?P<userId>[0-9a-f\-]{36})?[\/]?$', views.getUserTransactions),

	url(r'^request/(?P<itemId>[0-9a-f\-]{36})[\/]?$', views.request),
	url(r'^accept/(?P<tradeId>[0-9a-f\-]{36})[\/]?$', views.accept),
	url(r'^decline/(?P<tradeId>[0-9a-f\-]{36})[\/]?$', views.decline),

	url(r'^items[\/]?$', views.items),	
]
urlpatterns = format_suffix_patterns(urlpatterns)