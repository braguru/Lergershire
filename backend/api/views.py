from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from .serializers import RegisterSerializer, InvitationSerializer, UserSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from .models import User, Profile, InvitationEmail
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
import secrets
import string



# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
    

# Generates random password
def generate_random_password(length=8):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password



User = get_user_model()     # Get the customized User model
# @permission_classes([IsAdminUser])
class send_invitation(APIView):
    serializer_class = InvitationSerializer
    
    def post(self, request):
        email = request.data.get('email')   
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check if user with this email already exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # If user does not exist, create a new one
        if not user:
            username = email.split('@')[0]
            # password = User.objects.make_random_password()
            password = generate_random_password()
            user = User.objects.create_user(username=username, email=email, password=password)
        
        password = password

        # Send invitation email with link to login
        subject = 'Invitation to login'
        message = f'Hi {user.username},\n\nYou have been invited to login to our website. Please click the link below to login:\n\n{request.build_absolute_uri(reverse("login"))}\n\nYour username is {user.username} and your password is {password}. Please change your password after logging in.\n\nThanks,\nThe Website Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Log user in automatically
        # user = authenticate(username=user.email, password=password)
        # if user is not None:
        #     login(request, user)
        
        # Save the email in the InvitationEmail model
        InvitationEmail.objects.create(email=email)

        # Return serialized data
        serializer = self.serializer_class(user)
        return Response(serializer.data)


@api_view(['POST'])
def login_user(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
    # token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"user":serializer.data}) # return the data including the token




class Profile(viewsets.ModelViewSet):
    """Handles creating and updating profile"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
    
    



class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated)
    def put(self, request):
        # Create an instance of the serializer with the request data
        serializer = ChangePasswordSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Get the user making the request
            user = request.user

            # Get the current password, new password, and retype new password from the request data
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')
            retype_new_password = serializer.validated_data.get('retype_new_password')

            # Verify the current password
            if not user.check_password(current_password):
                return Response({'error': 'Invalid current password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new passwords match
            if new_password != retype_new_password:
                return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password for the user using set_password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        
        # If the serializer is not valid, return the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)