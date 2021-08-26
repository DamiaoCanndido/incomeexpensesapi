from django.db import models
from authentication.models import User 
from helpers.models import TrackingModel


class Income(TrackingModel):

    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE_HUSTLES', 'SIDE_HUSTLES'),
        ('OTHERS', 'OTHERS'),
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=15)
    amount = models.DecimalField(max_length=15, max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner)+ 's income'
