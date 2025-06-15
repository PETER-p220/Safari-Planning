from django.db import models
from django import forms 
class Booking(models.Model):
    user_id=models.IntegerField()
    tour_package_id=models.IntegerField()
    num_people=models.IntegerField()
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    status=models.TextField(max_length=30)
    total_amount=models.DecimalField(max_digits=20,decimal_places=2)