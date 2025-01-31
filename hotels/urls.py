from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('list', Hotel_ViewSet, basename= 'hotel')
router.register('rooms', RoomViewSet, basename= 'room')
router.register('room/list', Room_View, basename= 'room-list')
router.register('images', HotelImage_ViewSet, basename= 'hotel-img')
router.register('room_images', RoomImage_ViewSet, basename= 'room-img')

urlpatterns = [
    path('', include(router.urls)),
    # path('images/<hotel_id>/', HotelImage_View.as_view(), name= 'hotel-img'),
    
    
]