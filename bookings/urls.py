from django.urls import path
from .views import Booking_View, BookingHistory_View, RoomAvailable_View

urlpatterns = [
    path('bookings/', Booking_View.as_view(), name='booking-add'),
    path('bookings/history/', BookingHistory_View.as_view(), name='booking-history'),
    path('bookings/<int:pk>/', Booking_View.as_view(), name='booking-delete'),
    path('bookings/available/<int:hotel_id>/<int:room_id>/', RoomAvailable_View.as_view(), name='available-date'),
    

]

