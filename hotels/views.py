from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . models import Hotel_Model, HotelImage_Model, Room_Model, RoomImage_Model
from . serializers import Hotel_Serializer, HotelImage_Serializer, Room_Serializer, RoomImage_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from datetime import date
from bookings.models import Booking_Model
from django.contrib.postgres.search import TrigramSimilarity

# Create your views here.



class Hotel_ViewSet(ModelViewSet):
    queryset = Hotel_Model.objects.all()
    serializer_class = Hotel_Serializer
    
    

class HotelImage_ViewSet(ModelViewSet):
    queryset = HotelImage_Model.objects.all()
    serializer_class = HotelImage_Serializer
    
    
    
class RoomImage_ViewSet(ModelViewSet):
    queryset = RoomImage_Model.objects.all()
    serializer_class = RoomImage_Serializer
    

# ==========
class Room_View(ModelViewSet):
    queryset = Room_Model.objects.all()
    serializer_class = Room_Serializer

# ==========

        
        
# ==========
class RoomViewSet(ModelViewSet):
    queryset = Room_Model.objects.select_related('hotel').all()
    serializer_class = Room_Serializer


    def get_queryset(self):
        filters = Q()

        # Hotel ID Filter
        hotel_id = self.request.query_params.get('hotel_id')
        if hotel_id:
            if not hotel_id.isdigit():
                raise ValidationError({"error": "hotel_id must be a valid number."})
            filters &= Q(hotel_id= int(hotel_id))
        else:
            raise ValidationError({"error": "hotel_id is required."})


        # Room ID Filter
        room_id = self.request.query_params.get('room_id')
        if room_id:
            if not room_id.isdigit():
                raise ValidationError({"error": "room_id must be a valid number."})
            room_id = int(room_id)
            filters &= Q(id= room_id)


        # Search Filter
        search = self.request.query_params.get("search", "")
        if search:
            filters &= Q(room_type__icontains= search) | Q(hotel__city__icontains= search)


        # Guests Filter
        guests = self.request.query_params.get('guests', "")
        if guests:
            try:
                if guests.endswith('+'):
                    min_guests = int(guests[:-1])
                    filters &= Q(guests__gte= min_guests)
                else:
                    guests = int(guests)
                    filters &= Q(guests= guests)
            except ValueError:
                raise ValidationError({"error": "guests must be a valid number."})

        # Check-in and Check-out Date Filter
        check_in = self.request.query_params.get('check_in', "").strip()
        check_out = self.request.query_params.get('check_out', "").strip()
        if check_in and check_out:
            try:
                check_in_date = date.fromisoformat(check_in)
                check_out_date = date.fromisoformat(check_out)

                if check_in_date >= check_out_date:
                    raise ValidationError({"error": "Check-out date must be after check-in date."})

                booked_rooms = Booking_Model.objects.filter(
                    end_date__gt= check_in_date,
                    start_date__lt= check_out_date,
                    room__hotel_id= hotel_id  
                ).values_list("room_id", flat= True)

                filters &= ~Q(id__in= booked_rooms)

            except ValueError:
                raise ValidationError({"error": "Invalid date format. Use 'YYYY-MM-DD'."})

        # Sorting filter
        sort_option = self.request.query_params.get("sort", "").strip()
        if sort_option == "price-low":
            queryset = queryset.order_by("price_per_night")
        elif sort_option == "price-high":
            queryset = queryset.order_by("-price_per_night")
        elif sort_option == "latest":
            queryset = queryset.order_by("-create_time")


        return Room_Model.objects.filter(filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            hotel_id = self.request.query_params.get('hotel_id')
            
           
            check_in = self.request.query_params.get('check_in', "")
            check_out = self.request.query_params.get('check_out', "")
            
            if check_in and check_out:
                message = "No rooms are available for the selected dates."
            else:
                message = "No rooms match the given filters."
            
            return Response({
                "message": message,
                "note": f"Please check availability for other dates or filters in this hotel (hotel_id: {hotel_id})."
            }, status= status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many= True)
        return Response(serializer.data)




# http://127.0.0.1:8000/api/hotels/rooms/?hotel_id=2&check_in=2025-01-27&check_out=2025-01-29



