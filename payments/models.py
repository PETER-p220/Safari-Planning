from django.db import models
class Payment(models.Model):
    booking_id=models.IntegerField()
    payment_method=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=20,decimal_places=2)
    payment_date=models.TimeField(auto_now=False, auto_now_add=False)
    