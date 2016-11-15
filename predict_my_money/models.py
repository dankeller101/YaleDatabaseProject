from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100, default="")
    total_invested = models.IntegerField(default=0)
    liquid_assets = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Stock(models.Model):
    stock_name = models.CharField(max_length=10)
    current_high = models.IntegerField(default=0)
    current_low = models.IntegerField(default=0)
    general_trend = models.IntegerField(default=0)
    start_date = models.DateField('Earliest Record')
    end_date = models.DateField('Latest Record')

    def __str__(self):
        return self.stock_name

    def needs_update(self):
        return self.end_date < timezone.now()

    def how_many_days(self):
        return timezone.now() - self.end_date

class Stock_Owned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    bought_at = models.IntegerField(default=0)
    bought_on = models.DateTimeField('date bought')
    amount_owned = models.IntegerField(default=0)

    def __str__(self):
        return self.user + ' ' + self.stock

class Stock_Day(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    high = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)
    day = models.DateField('Day of Data')

    def __str__(self):
        return self.stock + ' ' + self.day



