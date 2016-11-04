from functools import wraps
import auth

def authenticate(function):
	@wraps(function)
	def wrappedFunc(request, *args, **kwargs):
		print function.__name__
		print request.data
		user = auth.verify(
				userId=request.META['HTTP_USERID'],
				authToken=request.META['HTTP_AUTHTOKEN'])
		if user:
			setattr(request, 'user', user)
			return function(request, *args, **kwargs)
		else:
			return JsonResponse(status=401)
	return wrappedFunc
		
