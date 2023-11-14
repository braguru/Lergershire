from rest_framework import serializers, status
from .models import User, InvitationEmail, Profile, Notification
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    phone_number = PhoneNumberField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number','password']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError("Username should contain only alphanumeric characters")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    

class InvitationSerializer(serializers.ModelSerializer):
   email = serializers.EmailField(max_length=255)
   class Meta:
       model = InvitationEmail
       fields = ['email']
       
       
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'email', 'password')
    

# class SettingsSerializer(serializers.ModelSerializer):
#     """A serializer for our user profile objects. """
#     profile_pic = serializers.SerializerMethodField()
#     # Investment_objectives = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Profile
#         fields = ('profile_pic', 'Investment_objectives')
        
        
        
class ProfileSerializer(serializers.ModelSerializer):
    # profile = SettingsSerializer()
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ('id', 'username', 'email', 'profile_pic', 'Investment_objectives')
        
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsOwnerOrReadOnly()]
        return []

   

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    retype_new_password = serializers.CharField(required=True)
    
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"