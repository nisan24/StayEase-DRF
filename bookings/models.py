from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel_Model, Room_Model
from django.core.exceptions import ValidationError
from datetime import date

PAYMENT_STATUS = [
    ("Pending", "Pending"),
    ("Paid", "Paid")
]

class Booking_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel_Model, on_delete= models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room_Model, on_delete= models.CASCADE, related_name="bookings", null= True)
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField(null= True, help_text="Number of guests")
    contact_number = models.CharField(max_length= 15, blank= True, null= True)
    email = models.EmailField(blank= True, null= True)
    total_price = models.DecimalField(max_digits= 10, decimal_places= 2, blank= True, null= True)
    total_nights = models.PositiveIntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length= 50, choices= PAYMENT_STATUS, default='Pending')
    payment_reference = models.CharField(max_length= 100, blank= True, null= True, help_text="Payment transaction ID")
    is_confirmed = models.BooleanField(default= False)
    booking_time = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-booking_time']

    def clean(self):
        if self.start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")
        
        bookings_date = Booking_Model.objects.filter(
            room= self.room,
            end_date__gt= self.start_date,
            start_date__lt= self.end_date
        ).exclude(id= self.id)
        
        if bookings_date.exists():
            raise ValidationError(f"This room is already booked between {self.start_date} and {self.end_date}.")
        
        if self.guests > self.room.guests:
            raise ValidationError(f"Maximum guests allowed for this room is {self.room.guests}.")

    def save(self, *args, **kwargs):
        self.clean()
        
        self.total_nights = (self.end_date - self.start_date).days
        self.total_price = self.room.price_per_night * self.total_nights

        if not self.id:
            if self.room.available_rooms < 1:
                raise ValidationError("Room is already fully booked.")
            self.room.available_rooms -= 1
            self.room.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} at {self.hotel.name} (Room: {self.room.room_type})"
