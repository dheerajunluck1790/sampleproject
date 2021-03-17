import requests,ast,jwt 
from django.conf import settings 
import http.client
from django.shortcuts import render
from rest_framework.views import APIView 
from django.contrib.auth import login,authenticate 
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import UserSerializer
from .services import generate_otp
from .models import User   
from rest_framework.pagination import LimitOffsetPagination
conn = http.client.HTTPConnection("2factor.in")
class UserSignUp(ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	pagination_class=LimitOffsetPagination
	def create(self,request):
		try:
			params=request.data 
			try:
				mobile_number=params.pop("mobile_number") 
			except Exception:
				mobile_number=None  
			params.update(mobile_number=mobile_number)
			mobile_number=str(mobile_number)
			user=User.objects.filter(mobile_number=mobile_number)
			if user:
				return Response({"status":False,"message":"It seems you are already registered with this mobile number,login with sent otp"},status=status.HTTP_400_BAD_REQUEST)
			'''
			if mobile number is already  registered we won't send otp ,as it affects our cost 
			'''
			otp=generate_otp(mobile_number)
			otp=str(otp)
			conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=30e2c0ec-86dd-11eb-a9bc-0200cd936042&to="+str(mobile_number)+"&otpvalue="+str(otp)+"&templatename=sample")
			res=conn.getresponse()
			data = res.read()
			data=data.decode("utf-8")
			data=ast.literal_eval(data)
			if data['Status']=='Success':
				try:
					serializer=UserSerializer(data=params)
					if serializer.is_valid(raise_exception=True):
						user=serializer.save()
						user.set_password(otp)
						user.save()
						return Response({"status":True,"message":"Signed Successful,We have sent an otp on your mobile number,It is your Password for login"},status=status.HTTP_201_CREATED) 
				except Exception:
					return Response({"status":False,"message":"Something went wrong","errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"status":False,"message":"Something went wrong from our side"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		except Exception:
			return Response({"status":False,'message':"OOPS,Something went wrong while signup"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
	def post(self,request):
		try:
			params=request.data 
			try:
				mobile_number=params.pop("mobile_number") 
			except Exception:
				mobile_number=None  
			if not mobile_number:
				return Response({"status":False,"message":"Mobile Number Not found"},status=status.HTTP_400_BAD_REQUEST)
			try:
				otp=params.pop("otp") 
			except Exception:
				otp=None 
			if not otp:
				return Response({"status":False,"message":"Otp Not Received"},status=status.HTTP_400_BAD_REQUEST)
			try:
				user=User.objects.get(mobile_number=mobile_number) 
			except Exception:
				return Response({"status":False,"message":"OOPS, We are not able to recognise you"},status=status.HTTP_400_BAD_REQUEST)
			user.is_active=True
			user.save()
			user=authenticate(mobile_number=mobile_number,password=otp)
			if not user:
				return Response({"status":False,"message":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
			auth_token=jwt.encode({"mobile_number":mobile_number},settings.SECRET_KEY)
			login(request,user)
			serializer=UserSerializer(user)
			data={"user":serializer.data,"token":auth_token}
			return Response({"status":True,"message":"Loged in Successfully","data":data},status=status.HTTP_200_OK)
		except Exception:
			return Response({"status":False,"message":"OOPS,Something went wrong while login"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
