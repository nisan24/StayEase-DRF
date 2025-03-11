# from rest_framework import serializers
# from django.contrib.auth.models import User
# from . models import *


# class UserRegistration_Serializers(serializers.ModelSerializer): 
#     first_name = serializers.CharField(required = True)
#     last_name = serializers.CharField(required = True)
#     confirm_password = serializers.CharField(write_only = True, required = True)
    
#     phone_number = serializers.CharField(required= True, max_length= 15)
#     address = serializers.CharField(required= False, allow_blank= True)
#     country = serializers.CharField(required= False, allow_blank= True)
#     profile_image = serializers.ImageField(required= False)
    
#     class Meta:
#         model = User
#         fields = [
#             'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 
#             'phone_number', 'address', 'city', 'country', 'profile_image'
#         ]
        
#     def save(self):
#         username = self.validated_data['username']
#         first_name = self.validated_data['first_name']
#         last_name = self.validated_data['last_name']
#         email = self.validated_data['email']
#         password = self.validated_data['password']
#         confirm_password = self.validated_data['confirm_password']
          
          
#         if password != confirm_password:
#             raise serializers.ValidationError({'error': "Passwords do not match"})
        
        
#         if User.objects.filter(username= username).exists():
#             raise serializers.ValidationError({'username': 'username already exists'})
        
        
#         if User.objects.filter(email= email).exists():
#             raise serializers.ValidationError({'email': 'Email already exists'})
        
        
#         account = User(username = username, first_name = first_name, last_name = last_name, email = email)
#         account.set_password(password)
#         account.is_active = False
#         account.save()
#         return account
    
    
    
# class UserLogin_Serializer(serializers.Serializer):
#     username = serializers.CharField(required = True)
#     password = serializers.CharField(required = True)
    
    
    
    
# class UserProfile_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']
        
       
       
        
        
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile_Model

class UserRegistration_Serializers(serializers.ModelSerializer):
    first_name = serializers.CharField(required= True)
    last_name = serializers.CharField(required= True)
    confirm_password = serializers.CharField(write_only= True, required= True)

    phone_number = serializers.CharField(required= True, max_length= 15)
    address = serializers.CharField(required= False, allow_blank= True)
    city = serializers.CharField(required= False, allow_blank= True)
    profile_image = serializers.ImageField(required= False, allow_null= True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 
            'phone_number', 'address', 'city', 'profile_image'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        if User.objects.filter(username= validated_data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        if User.objects.filter(email= validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        user = User.objects.create_user(
            username= validated_data['username'],
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
            email= validated_data['email'],
            password= validated_data['password']
        )

        user.is_active = False
        user.save()

        UserProfile_Model.objects.create(
            user= user,
            phone_number= validated_data.get('phone_number'),
            address= validated_data.get('address'),
            city= validated_data.get('city'),
            profile_image= validated_data.get('profile_image', None)
        )

        return user

    
class UserLogin_Serializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    
    
    
class UserProfile_Serializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    
    class Meta:
        model = UserProfile_Model
        fields = [
            "username", "first_name", "last_name", "email",
            "phone_number", "address", "city", "profile_image", "join_date"
        ]
        
    