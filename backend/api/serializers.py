from rest_framework import serializers, status
from .models import User, InvitationEmail, Profile
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.response import Response


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    phone_number = PhoneNumberField()
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'phone_number', 'password', 'fund_type', 'amount_to_invest', 'investment_objectives']
        
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
       
      
      
class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = ('id', 'username', 'email', 'profile_pic', 'phone_number','investment_objectives')
    
   
 
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'fund_type', 'amount_to_invest', 'investment_objectives')
        extra_kwargs = {'password': {'write_only':True}}

        


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    retype_new_password = serializers.CharField(required=True)
