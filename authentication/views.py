from rest_framework import generics
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from rest_framework import response, serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterAPIView(GenericAPIView):

    authentication_classes = []

    serializer_class = RegisterSerializer

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


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
