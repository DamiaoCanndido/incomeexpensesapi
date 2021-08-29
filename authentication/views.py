from rest_framework.generics import GenericAPIView
from rest_framework.serializers import Serializer
from authentication.serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer, RequestPasswordResetEmailSerializer
from rest_framework import response, status, views
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from .renderers import UserRenderer
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from authentication.utils import Util


class RegisterAPIView(GenericAPIView):

    authentication_classes = []

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self ,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.username+' Use link below to verify your email \n'+absurl
            data={'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your e-mail'}
            Util.send_email(data)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
            return response.Response({'message': 'Successfully activated.'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as id:
            return response.Response({'error': 'Activation expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as id:
            return response.Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(GenericAPIView):

    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hi Use link below to reset your password \n'+absurl
            data={'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return response.Response({'success': 'We have sent you a link to reset your password.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, uidb64, token):
        pass


