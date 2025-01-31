from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review_Model
from hotels.models import Hotel_Model, Room_Model
from .serializers import Review_Serializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class Review_View(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, hotel_id= None, room_id= None, *args, **kwargs):
        if hotel_id:
            reviews = Review_Model.objects.filter(hotel_id= hotel_id)
        elif room_id:
            reviews = Review_Model.objects.filter(room_id= room_id)
        else:
            return Response({"detail": "Provide hotel_id or room_id to fetch reviews."}, status= status.HTTP_400_BAD_REQUEST)

        serializer = Review_Serializer(reviews, many= True)
        return Response({
            "reviews": serializer.data,
            "total_reviews": reviews.count()
        })


    def post(self, request, hotel_id= None, room_id= None, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required!"}, status= status.HTTP_401_UNAUTHORIZED)

        hotel = None
        room = None
        if hotel_id:
            hotel = get_object_or_404(Hotel_Model, id= hotel_id)
            if Review_Model.objects.filter(user= request.user, hotel= hotel).exists():
                return Response({"detail": "You have already reviewed this hotel!"}, status= status.HTTP_400_BAD_REQUEST)
        if room_id:
            room = get_object_or_404(Room_Model, id= room_id)
            if Review_Model.objects.filter(user= request.user, room= room).exists():
                return Response({"detail": "You have already reviewed this room!"}, status= status.HTTP_400_BAD_REQUEST)

        data = {
            "user": request.user.id,
            "hotel": hotel.id if hotel else None,
            "room": room.id if room else None,
            "rating": request.data.get("rating"),
            "comment": request.data.get("comment"),
        }

        serializer = Review_Serializer(data= data)
        if serializer.is_valid():
            serializer.save(user= request.user, hotel= hotel, room= room)
            return Response({"message": "Review added successfully!", "data": serializer.data}, status= status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


    def put(self, request, hotel_id= None, room_id= None, review_id= None, *args, **kwargs):
        if hotel_id:
            review = get_object_or_404(Review_Model, id= review_id, hotel_id= hotel_id)
        elif room_id:
            review = get_object_or_404(Review_Model, id= review_id, room_id= room_id)
        else:
            return Response({"error": "Provide hotel_id or room_id to identify the review."}, status= status.HTTP_400_BAD_REQUEST)

        if review.user != request.user:
            return Response(
                {"error": "You can only edit your own reviews."},
                status= status.HTTP_403_FORBIDDEN
            )

        serializer = Review_Serializer(review, data= request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Review updated successfully!", "data": serializer.data},
                status= status.HTTP_200_OK
            )

        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hotel_id= None, room_id= None, review_id= None, *args, **kwargs):
        if hotel_id:
            review = get_object_or_404(Review_Model, id= review_id, hotel_id= hotel_id)
        elif room_id:
            review = get_object_or_404(Review_Model, id= review_id, room_id= room_id)
        else:
            return Response({"error": "Provide hotel_id or room_id to identify the review."}, status= status.HTTP_400_BAD_REQUEST)

        if review.user != request.user:
            return Response(
                {"error": "You can only delete your own reviews."},
                status= status.HTTP_403_FORBIDDEN
            )

        review.delete()
        return Response({"message": "Review deleted successfully!"}, status= status.HTTP_204_NO_CONTENT)



    # def put(self, request, review_id, *args, **kwargs):
    #     review = get_object_or_404(Review_Model, id= review_id, user= request.user)
    #     serializer = Review_Serializer(review, data= request.data, partial= True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Review updated successfully!", "data": serializer.data}, status= status.HTTP_200_OK)

    #     return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, review_id, *args, **kwargs):
    #     review = get_object_or_404(Review_Model, id= review_id, user= request.user)
    #     review.delete()
    #     return Response({"message": "Review deleted successfully!"}, status= status.HTTP_204_NO_CONTENT)


