from testapp import views
from rest_framework.routers import DefaultRouter 
router=DefaultRouter(trailing_slash=False)
router.register("",views.UserSignUp,basename="signup")