from rest_framework import serializers
from .models import User, InvitationEmail, Setting, Notification


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
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
    

class SettingsSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects. """
    class Meta:
        model = Setting
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'website', 'bio']
        

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    retype_new_password = serializers.CharField(required=True)
    
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"