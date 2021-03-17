from django.utils.deprecation import MiddlewareMixin 
from rest_framework.response import Response 
from rest_framework import status 
class DisableCsrf(MiddlewareMixin):
	def proccess_request(self,request):
		setattr(request,"_dont_enforce_csrf_check",True)
class DisableCors(MiddlewareMixin):
	def proccess_response(self,request):
		response['Acess-Control-Allow-Origin']=True 
		response['Access-Control-Allow-Headers']=True 
