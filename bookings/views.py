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
from datetime import date
# Create your views here.

class Booking_View(APIView):
    permission_classes = [IsAuthenticated]
    
    
    # def get(self, request):
    #     bookings = Booking_Model.objects.filter(user= request.user)
    #     serializer = Booking_Serializer(bookings, many= True)
    #     return Response({"history": serializer.data})

    
    def post(self, request):
        serializer = Booking_Serializer(data= request.data)
        if serializer.is_valid():
            try:
                serializer.save(user= request.user)
                return Response(serializer.data, status= status.HTTP_201_CREATED)
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
    def get(self, request):
        bookings = Booking_Model.objects.filter(user= request.user)
        serializer = Booking_Serializer(bookings, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)




class RoomAvailable_View(APIView):
    def get(self, request, hotel_id, room_id):
        try:
            hotel = Hotel_Model.objects.get(id= hotel_id)
        except Hotel_Model.DoesNotExist:
            return Response(
                {"error": f"No hotel found. ID {hotel_id}."},
                status= status.HTTP_404_NOT_FOUND
            )

        try:
            room = Room_Model.objects.get(id= room_id, hotel_id= hotel_id)
        except Room_Model.DoesNotExist:
            return Response(
                {"error": f"No room found. ID {room_id} for hotel ID {hotel_id}."},
                status= status.HTTP_404_NOT_FOUND
            )
            
            
        bookings = Booking_Model.objects.filter(hotel_id= hotel_id, room_id= room_id).values("start_date", "end_date")
        
        if not bookings:
            return Response(
                {"message": "This room is available for all dates."},
                status= status.HTTP_200_OK
            )

        return Response(
            {"booked_dates": list(bookings)},
            status= status.HTTP_200_OK
        )




# function renderBookings(bookings) {
#     bookings.forEach(booking => {
#         const deleteButton = document.createElement('button');
#         deleteButton.innerText = "Delete";

#         if (booking.is_confirmed) {
#             deleteButton.disabled = true;  // Disable delete button
#         } else {
#             deleteButton.onclick = () => deleteBooking(booking.id); // Allow delete
#         }

#         document.body.appendChild(deleteButton);
#     });
# }
