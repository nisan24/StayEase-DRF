from django.db import models
from hotels.models import Hotel_Model, Room_Model
from django.contrib.auth.models import User

# Create your models here.
RATING_CHOICES = [
    ("⭐", 1),
    ("⭐⭐", 2),
    ("⭐⭐⭐", 3),
    ("⭐⭐⭐⭐", 4),
    ("⭐⭐⭐⭐⭐", 5),
]


class Review_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="user_reviews")
    hotel = models.ForeignKey(Hotel_Model, on_delete= models.CASCADE, related_name="hotel_reviews", null= True, blank= True)
    room = models.ForeignKey(Room_Model, on_delete= models.CASCADE, related_name="room_reviews", null= True, blank= True)
    rating = models.CharField(max_length= 8, choices= RATING_CHOICES)  
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add= True)
    update_time = models.DateTimeField(auto_now= True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ["user", "hotel"], name="unique_hotel_review"),
            models.UniqueConstraint(fields= ["user", "room"], name="unique_room_review"),
        ]
        ordering = ["-create_time"]

    def __str__(self):
        if self.hotel:
            return f"Review by {self.user.username} for Hotel: {self.hotel.name}"
        elif self.room:
            return f"Review by {self.user.username} for Room: {self.room.room_type}"
        return f"Review by {self.user.username}"

