from authentication.utils import Util
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


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


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs['data'].get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=attrs['data'].get('request')).domain
                relativeLink = reverse('email-verify')
                absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                email_body = 'Hi '+user.username+' Use link below to verify your email \n'+absurl
                data={'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your e-mail'}
                Util.send_email(data)
            return attrs
        except ValueError:
            print('Error')
        
        return super().validate(attrs)

