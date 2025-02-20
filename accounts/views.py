from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, EmailMessage
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfile_Serializer, UserRegistration_Serializers
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile_Model
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponseRedirect

# Create your views here.

class UserRegistrationAPIView(APIView):    
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserRegistration_Serializers
    
    def post(self, req):
        serializer = self.serializer_class(data= req.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://stay-ease-drf.vercel.app/api/accounts/verify/{uid}/{token}/"
            
            email_subject = "Activate your account"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message" : "Registration successful. Please check your email for verification."})
        
        return Response(serializer.errors)
            
            
            
def activate(req, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('user_login')
        return HttpResponseRedirect("https://stayease.vercel.app/login.html")
        
    else:
        return HttpResponseRedirect("https://stayease.vercel.app/register.html")
        # return redirect('register')
        # return redirect('register', {'message': 'Invalid or expired token.'})
        
        
        
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLogin_Serializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            if user:
                if not user.is_active:
                    return Response({'error': "Your account is not activated. Please check your email."})
                
                token, _ = Token.objects.get_or_create(user = user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id, 'username': user.username , 'name': user.first_name + str(" ") + user.last_name, "message": "Login successful"})
            else:
                return Response({'error' : "Invalid credentials"})
        return Response(serializer.errors) 
            


# class UserLogoutApiView(APIView):
#     def get(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         return redirect('user_login') 


class UserLogoutApiView(APIView):
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass
        logout(request)
        return redirect('user_login') 



class UserProfile_ViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = UserProfile_Model.objects.all() 
    serializer_class = UserProfile_Serializer
    
    def get_queryset(self):
        # print(f"User: {self.request.user}") 
        return UserProfile_Model.objects.filter(user= self.request.user)

