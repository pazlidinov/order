from django.db import models


# Create your models here.
class Customer(models.Model):    
    username = models.CharField(max_length=150)
    name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    offer_link = models.CharField(max_length=250, null=True)
    invited = models.IntegerField(default=0)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.username)
