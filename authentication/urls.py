from authentication import views
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
]