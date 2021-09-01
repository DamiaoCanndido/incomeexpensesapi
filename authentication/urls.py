from authentication import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('reset-password-complete', views.SetNewPasswordAPIView.as_view(), name='reset-password-complete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]