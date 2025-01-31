from rest_framework import serializers
from .models import *

class Review_Serializer (serializers.ModelSerializer):
    user = serializers.CharField(source= 'user.username', read_only= True)
    hotel_name = serializers.CharField(source= 'hotel.name', read_only= True)
    room_type = serializers.CharField(source='room.room_type', read_only= True, allow_null= True) 
    class Meta:
        model = Review_Model
        fields = ['id', 'user', 'hotel', 'room', 'room_type', 'hotel_name', 'rating', 'comment', 'create_time']        
        
        