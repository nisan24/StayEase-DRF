from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . views import *



router = DefaultRouter()
router.register('profile', UserProfile_ViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("register/", UserRegistrationAPIView.as_view(), name= 'register'),
    path('login/', UserLoginApiView.as_view(), name= 'user_login'),
    path('logout/', UserLogoutApiView.as_view(), name= 'logout'),
    path('verify/<str:uid64>/<str:token>/', activate, name= 'activate'),
    # path('profile/', UserProfileView.as_view(), name='user_profile'),

]
