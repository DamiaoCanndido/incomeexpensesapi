from django.contrib import auth
from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.pop('confirm_password', '')
        if password != confirm_password:
            raise serializers.ValidationError(detail='Password do not match.', code=400)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=128, min_length=5, read_only=True)
    email = serializers.EmailField(max_length=128, min_length=5)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=555, min_length=5, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled.')
        if not user.email_verified:
            raise AuthenticationFailed('Email is not verified.')
        return {'username': user.username, 'email': user.email, 'tokens': user.tokens}
        
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'tokens',)

