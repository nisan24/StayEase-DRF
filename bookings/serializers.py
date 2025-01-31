from rest_framework import serializers
from .models import Booking_Model

class Booking_Serializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only= True) 
    hotel_name = serializers.CharField(source='hotel.name', read_only= True)
    room_type = serializers.CharField(source='room.room_type', read_only= True)

    class Meta:
        model = Booking_Model
        fields = [
            'id', 'user', 'hotel', 'hotel_name', 'room', 'room_type', 'start_date', 'end_date',
            'guests', 'contact_number', 'email', 'total_price', 'total_nights', 'payment_status',
            'payment_reference', 'is_confirmed', 'booking_time'
        ]
        read_only_fields = [
            'user', 'hotel_name', 'room_type', 'total_price', 'total_nights', 'payment_status',
            'is_confirmed', 'booking_time'
        ]





# class Booking_Serializer(serializers.ModelSerializer):
#     user = serializers.CharField(source= 'user.username', read_only= True)
#     hotel_name = serializers.CharField(source= 'hotel.name', read_only= True)
#     class Meta:
#         model = Booking_Model
#         fields = '__all__'
#         read_only_fields = ('user', 'hotel_name', 'room', 'total_price', 'total_nights', 'payment_status', 'is_confirmed')
    




# json post request
# {
#     "hotel": 1,
#     "room": 10,
#     "start_date": "2025-02-01",
#     "end_date": "2025-02-05",
#     "guests": 2,
#     "contact_number": "0123456789",
#     "email": "nisan@gmail.com"
# }



# output
# {
#     "id": 5,
#     "user": "nisan",
#     "hotel": 1,
#     "hotel_name": "Grand Paradise Hotel",
#     "room": 10,
#     "room_type": "Deluxe",
#     "start_date": "2025-02-01",
#     "end_date": "2025-02-05",
#     "guests": 2,
#     "contact_number": "0123456789",
#     "email": "nisan@gmail.com",
#     "total_price": "800.00",
#     "total_nights": 4,
#     "payment_status": "Pending",
#     "payment_reference": null,
#     "is_confirmed": false,
#     "booking_time": "2025-01-22T12:00:00Z"
# }
