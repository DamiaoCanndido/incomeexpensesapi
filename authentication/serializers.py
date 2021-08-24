from django.contrib import auth
from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

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

    email = serializers.EmailField(max_length=128, min_length=5, write_only=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user.is_active:
            raise AuthenticationFailed('Account disabled.')
        if not user.email_verified:
            raise AuthenticationFailed('Email is not verified.')
        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        return {'username': user.username, 'email': user.email, 'tokens': {}}
        
    '''
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token',)
    '''

        # read_only_fields = ['token']
