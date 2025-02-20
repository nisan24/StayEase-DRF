from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class UserProfile_Model(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length= 15, blank= True, null= True)
    address = models.TextField(blank= True, null= True)
    city = models.CharField(max_length= 50, blank= True, null= True)
    # profile_image = models.ImageField(upload_to="accounts/profile_images/", blank= True, null= True, default= "accounts/default_profile.jpg")
    profile_image = CloudinaryField('accounts/profile_images', null= True, blank= True)
    join_date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.user.username} -- Profile"
