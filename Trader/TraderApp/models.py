from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
# Create your models here.

class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__ (self):
		return self.user.username

class Asset(models.Model):
	asset_id = models.CharField(max_length = 50)
	asset_name = models.CharField(max_length = 100)

	def __str__ (self):
		return self.asset_id


class Transaction(models.Model):
	user_from = models.ForeignKey(Person, on_delete=models.CASCADE,null=True, related_name='sender')
	user_to = models.ForeignKey(Person, on_delete=models.CASCADE,null=True, related_name='reciever')
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE ,null=True)
	units = models.DecimalField(max_digits=8,decimal_places=2,default=Decimal('0.00'))
	date = models.DateField(default=datetime.date.today)