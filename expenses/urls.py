from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseDetailListAPIView.as_view(), name='expense')
]