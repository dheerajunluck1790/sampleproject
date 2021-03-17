from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser 
from django.contrib.auth.models import PermissionsMixin, BaseUserManager 
class UserManager(BaseUserManager):
	def create_superuser(self,mobile_number,password):
		'''
		custom functions for creation of superuser 
		'''
		user=self.model(mobile_number=mobile_number)
		user.set_password(password)
		user.is_staff=True 
		user.is_superuser=True 
		user.is_active=True 
		user.save(using=self._db)
		return user 
class User(AbstractBaseUser,PermissionsMixin):
	first_name=models.CharField("User First Name",max_length=50,null=False,blank=False)
	middle_name=models.CharField("User Middle Name",max_length=50,null=True,blank=True)
	last_name=models.CharField("User Last Name",max_length=50,null=False,blank=False)
	mobile_number=models.BigIntegerField("User Mobile Number",null=False,blank=False,unique=True,error_messages={"unique":"OOPS,An User  with this mobile is already regsitered"})
	is_superuser=models.BooleanField("Is staff",default=False)
	is_staff=models.BooleanField("Is staff",default=False)
	is_active=models.BooleanField("Is active",default=False)
	country=models.CharField("country",default="India",max_length=50)
	objects=UserManager()
	USERNAME_FIELD="mobile_number"
	full_name=models.CharField("User Full Name",max_length=150,null=True,blank=True)
	def get_full_name(self):
		if self.middle_name:
			return "{} {} {}".format(self.first_name,self.middle_name,self.last_name)

		return "{} {}".format(self.first_name,self.last_name)
	def  save(self,*args,**kwargs):
		mobile_number=self.mobile_number
		full_name=self.get_full_name()
		super(User,self).save(*args,**kwargs)
	def __str__(self):
		return str(self.mobile_number)
