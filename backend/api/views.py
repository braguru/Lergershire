from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from .serializers import RegisterSerializer, InvitationSerializer, UserSerializer, ProfileSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.response import Response
from .models import User, Profile, InvitationEmail
from django.contrib.auth import authenticate, login, logout
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
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.utils.http import urlsafe_base64_encode

import secrets
import string



# Create your views here.
@api_view()
def Routes(request):
    return Response({
        "register : http://127.0.0.1:8000/api/register/",
        "login : http://127.0.0.1:8000/api/login/",
        "send_invitation : http://127.0.0.1:8000/api/send_invitation/", 
        "change_password : http://127.0.0.1:8000/api/change_password/",
        "profile : http://127.0.0.1:8000/api/profile/",
        "logout : http://127.0.0.1:8000/api/logout/",
    })

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
            
            
        password = ''
        # If user does not exist, create a new one
        if not user:
            username = email.split('@')[0]
            phone_number = ""
            fund_type = ""
            amount_to_invest = 0
            investment_objectives = ""
            # password = User.objects.make_random_password()
            password = generate_random_password()
            user = User.objects.create_user(username=username, email=email, password=password, phone_number=phone_number, fund_type=fund_type, amount_to_invest=amount_to_invest, investment_objectives=investment_objectives)
        
        

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
    # Assuming you have a custom User model with an 'email' field
    user = get_object_or_404(User, email=request.data.get('email'))
    data = request.data
    data['username'] = request.data.get('email')

    # Check if the provided password is correct
    if not user.check_password(request.data.get('password')):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # If the password is correct, generate or get the user's token
    token, created = Token.objects.get_or_create(user=user)

    # Serialize the user data (you might want to customize the serializer)
    serializer = UserSerializer(instance=user, data=data)
    
    if serializer.is_valid(raise_exception=True):
        login(request, user)

    # Return the user data along with the token
    return Response({"user": serializer.data, "token": token.key})


class logout_user(APIView):
    """
    API View for user logout.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        """
        API endpoint for user logout.
        This view handles user logout by logging out the current user.
        Parameters:
        - request: The HTTP request object for user logout.
        Returns:
        - Returns a response with HTTP 200 OK, indicating a successful logout.
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
    
class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        # Assuming you have a one-to-one relationship between User and Profile
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    
    def put(self, request):
        # Create an instance of the serializer with the request data
        serializer = self.serializer_class(data=request.data)

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
    
    