from django.db import models
class Providers(models.Model):
    user_id=models.IntegerField()
    company_name=models.CharField()
    licence_no=models.CharField()
    address=models.CharField()
    status=models.CharField(max_length=50)
    def __str__(self):
        return self.user_id
    
