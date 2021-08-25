from django.db import models
from authentication.models import User 
from helpers.models import TrackingModel


class Expense(TrackingModel):

    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('RENT', 'RENT'),
        ('OTHERS', 'OTHERS'),
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=15)
    amount = models.DecimalField(max_length=15, max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
