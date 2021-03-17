from random import randint 
def generate_otp(mobile_number):
	otp=""
	for i in range(6):
		num=randint(1,9)
		otp=otp+str(num)
	return otp
