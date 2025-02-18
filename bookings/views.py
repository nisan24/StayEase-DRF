from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking_Model
from .serializers import Booking_Serializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from hotels.models import Hotel_Model, Room_Model
from django.db.models import Q
from datetime import date, datetime
from reviews.models import Review_Model
from reviews.serializers import Review_Serializer
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class Booking_View(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    
    # def get(self, request):
    #     bookings = Booking_Model.objects.filter(user= request.user)
    #     serializer = Booking_Serializer(bookings, many= True)
    #     return Response({"history": serializer.data})

    
    def post(self, request):
        serializer = Booking_Serializer(data= request.data)
        if serializer.is_valid():
            try:
                serializer.save(user= request.user)
                return Response({"booking": serializer.data}, status= status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        booking = get_object_or_404(Booking_Model, pk= pk, user= request.user)
        if booking.is_confirmed:
            return Response(
                {"error": "You cannot cancel a completed booking."},
                status= status.HTTP_403_FORBIDDEN,
            )
        if booking.room:
            booking.room.available_rooms += 1
            booking.room.save()
            
            
        booking.delete()
        return Response({"message": "Booking cancel successfully"}, status= status.HTTP_204_NO_CONTENT)




class BookingHistory_View(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        bookings = Booking_Model.objects.filter(user_id= user_id)
        serializer = Booking_Serializer(bookings, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)




class RoomAvailable_View(APIView):
    def get(self, request, hotel_id, room_id):
        try:
            hotel = Hotel_Model.objects.get(id= hotel_id)
        except Hotel_Model.DoesNotExist:
            return Response({"error": f"No hotel found with ID {hotel_id}."},
                            status= status.HTTP_404_NOT_FOUND)

        try:
            room = Room_Model.objects.get(id= room_id, hotel_id= hotel_id)
        except Room_Model.DoesNotExist:
            return Response({"error": f"No room found with ID {room_id} for hotel ID {hotel_id}."},
                            status= status.HTTP_404_NOT_FOUND)

        bookings = Booking_Model.objects.filter(hotel_id= hotel_id, room_id= room_id).values("start_date", "end_date")

        if not bookings.exists():
            return Response({"message": "This room is available for all dates."},
                            status= status.HTTP_200_OK)

        return Response({"booked_dates": list(bookings)}, status= status.HTTP_200_OK)



class Calculate_Checkout(APIView):
    def post(self, request):
        try:
            hotel_id = request.data.get("hotel_id")
            room_id = request.data.get("room_id")
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
            guests = int(request.data.get("guests"))

            if not (hotel_id and room_id and start_date and end_date and guests):
                return Response({"error": "All fields are required"}, status=400)

            try:
                hotel = Hotel_Model.objects.get(id=hotel_id)
                room = Room_Model.objects.get(id=room_id, hotel=hotel)
            except (Hotel_Model.DoesNotExist, Room_Model.DoesNotExist):
                return Response({"error": "Hotel or Room not found"}, status=404)

            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format, expected YYYY-MM-DD"}, status= 400)

            if start_date < datetime.today().date():
                return Response({"error": "Start date cannot be in the past"}, status= 400)

            if end_date <= start_date:
                return Response({"error": "End date must be after start date"}, status= 400)

            existing_bookings = room.bookings.filter(
                end_date__gte= start_date,
                start_date__lte= end_date
            )
            if existing_bookings.exists():
                return Response({"error": "This room is not available for the selected dates"}, status=400)

            if guests > room.guests:
                return Response({"error": f"Maximum guests allowed for this room is {room.guests}"}, status=400)

            total_nights = (end_date - start_date).days
            total_price = total_nights * room.price_per_night
            
            
            reviews = Review_Model.objects.filter(hotel= hotel_id, room= room_id)
            reviews_data = Review_Serializer(reviews, many= True).data


            return Response({
                "hotel_id": hotel.id,
                "hotel_name": hotel.name,
                "room_id": room.id,
                "room_type": room.room_type,
                "room_title": room.title,
                "room_reviews": reviews_data,
                "room_image": room.image.url if room.image else None,
                "start_date": start_date,
                "end_date": end_date,
                "guests": guests,
                "total_nights": total_nights,
                "price_per_night": room.price_per_night,
                "total_price": total_price
            })

        except Exception as e:
            return Response({"error": str(e)}, status= 500)
        
    
    
    