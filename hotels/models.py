from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_image(value):
    file_extension = value.name.split('.')[-1].lower()
    if file_extension not in ['jpg', 'jpeg', 'png']:
        raise ValidationError("Invalid image format. Only JPG, JPEG, and PNG are allowed.")
    return value   


class Hotel_Model(models.Model):
    name = models.CharField(max_length= 200)
    address = models.TextField()
    city = models.CharField(max_length= 100)
    country = models.CharField(max_length= 100, default= 'Bangladesh')
    description = models.TextField()
    amenities = models.TextField()
    price_range_min = models.DecimalField(max_digits= 10, decimal_places= 2, null= True)
    price_range_max = models.DecimalField(max_digits= 10, decimal_places= 2, null= True)
    total_rooms = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hotels/image/')
    create_time = models.DateTimeField(auto_now_add= True)

        
    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"




class HotelImage_Model(models.Model):
    hotel = models.ForeignKey(Hotel_Model , on_delete= models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/extra_images/', validators= [validate_image])
    time = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Image for {self.hotel.name}"
    
    
   
# ================


class Room_Model(models.Model):
    hotel = models.ForeignKey(Hotel_Model, on_delete= models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length= 100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits= 10, decimal_places= 2)
    amenities = models.TextField()
    guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    beds = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField(default= 1)
    title = models.CharField(max_length= 255, blank= True, null= True, help_text= "Room title")
    subtitle = models.TextField(blank= True, null= True, help_text="Room subtitle")
    available_rooms = models.PositiveIntegerField()
    image = models.ImageField(upload_to='rooms/image/', blank= True, null= True)
    create_time = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"
    
    
    


class RoomImage_Model(models.Model):
    room = models.ForeignKey(Room_Model, on_delete= models.CASCADE, related_name='room_images')
    image = models.ImageField(upload_to='rooms/extra_images/', validators= [validate_image])
    time = models.DateTimeField(auto_now_add= True)



    def __str__(self):
        return f"Image for {self.room.room_type} -- {self.room.hotel.name}"

    
    
    
# 'id', 'hotel', 'hotel_name', 'room_type', 'description', 'price_per_night', 'amenities', 'guests', 'bedrooms', 'beds', 'bathrooms', 'available_rooms', 'image', 'create_time'