from .views import ExpenseSummaryStats
from django.urls import path


urlpatterns = [
    path('expense-category-data', ExpenseSummaryStats.as_view(), name='expense-category-data')
]