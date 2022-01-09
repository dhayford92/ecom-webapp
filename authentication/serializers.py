from django.db.models import fields
from rest_framework import serializers
from .models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=80, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            return ValueError({'email', ('Email is already taken, Please try again with different email!')})
        return attrs
    
    def perform_create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=80, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'tokens']
        read_only_fields = ['name','tokens']
        
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['id']