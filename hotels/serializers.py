from rest_framework import serializers
from .models import Hotel_Model, HotelImage_Model, Room_Model, RoomImage_Model
from reviews.models import Review_Model
from reviews.serializers import Review_Serializer




class HotelImage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage_Model
        fields = ['id', 'image']


class RoomImage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage_Model
        fields = ['id', 'image']



class Hotel_Serializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    images = HotelImage_Serializer(many= True, read_only= True)

    class Meta:
        model = Hotel_Model
        fields = [
            'id', 'name', 'address', 'city', 'country', 'description', 
            'amenities', 'price_range_min', 'price_range_max', 'total_rooms', 
            'image', 'create_time', 'reviews', 'images'
        ]
        
    def get_reviews(self, obj):
        reviews = Review_Model.objects.filter(hotel= obj)
        return Review_Serializer(reviews, many= True).data



    
class Room_Serializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only= True)
    reviews = serializers.SerializerMethodField()
    room_images = RoomImage_Serializer(many= True, read_only= True)

    class Meta:
        model = Room_Model
        fields = [
            'id', 'hotel', 'hotel_name', 'room_type', 'title', 'subtitle', 'description', 'price_per_night', 
            'amenities', 'guests', 'bedrooms', 'beds', 'bathrooms', 
            'available_rooms', 'image', 'create_time', 'reviews', 'room_images'
        ]

    def get_reviews(self, obj):
        reviews = Review_Model.objects.filter(room= obj)
        return Review_Serializer(reviews, many= True).data
  
  
  