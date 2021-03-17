from rest_framework import serializers 
from testapp.models import User 
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User 
		fields=("first_name",'middle_name','last_name','mobile_number','full_name',"country")
