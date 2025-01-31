from django.urls import path
from . views import *

urlpatterns = [
    # GET hotel reviews
    path('hotel/<int:hotel_id>/', Review_View.as_view(), name='hotel-reviews'),
    # GET room reviews
    path('room/<int:room_id>/', Review_View.as_view(), name='room-reviews'),
    
    # POST hotel review
    path('hotel/<int:hotel_id>/add/', Review_View.as_view(), name='add-hotel-review'),
    # POST room review
    path('room/<int:room_id>/add/', Review_View.as_view(), name='add-room-review'),
    
    # PUT or DELETE hotel review
    path('<int:hotel_id>/<int:review_id>/', Review_View.as_view(), name='hotel-review-detail'),
    # PUT or DELETE room review
    path('<int:room_id>/<int:review_id>/', Review_View.as_view(), name='room-review-detail'),
]


# api/reviews/hotel/<hotel_id>/  hotel er review
# api/reviews/room/<room_id>/  ---- > room er review

# api/reviews/hotel/<hotel_id>/add/   --- hotel review POST
# api/reviews/room/<room_id>/add/  ---- room review POST

# api/reviews/hotel/<hotel_id>/<review_id>/   ----  hotel review PUT / delete
# api/reviews/room/<room_id>/<review_id>/    ----- room review put / delete