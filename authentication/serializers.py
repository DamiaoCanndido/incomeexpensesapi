from django.contrib import auth
from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
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
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

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

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    confirm_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)


    class Meta:
        fields = ['password', 'confirm_password', 'token', 'uidb64']


    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if password != confirm_password:
                raise serializers.ValidationError(detail='Password do not match.', code=400)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is not invalid', 400)

            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 400)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs 

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist() 
        except TokenError:
            self.fail('bad_token')

