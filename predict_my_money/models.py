from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + self.user.last_name

class Portfolio(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True)
    portfolio_name = models.CharField(max_length=255)
    current_diversity = models.FloatField(default=0)
    current_value = models.FloatField(default=0)
    total_invested = models.IntegerField(default=0)
    start_date = models.DateField('Creation Date of Portfolio', null=True)
    end_date = models.DateField('Latest Record')

    def __str__(self):
        return self.portfolio_name


class Portfolio_Day(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    day = models.DateField('Current Day')
    value = models.IntegerField(default=0)
    diversity = models.FloatField(default=0.0)

    def __str__(self):
        return self.day

class Stock(models.Model):
    stock_name = models.CharField(max_length=10)
    company_name = models.CharField(max_length=255, null=True)
    company_meta = models.TextField(null=True)
    current_high = models.IntegerField(default=0)
    current_low = models.IntegerField(default=0)
    current_adjusted_close = models.IntegerField(default=0)
    start_date = models.DateField('Earliest Record')
    end_date = models.DateField('Latest Record')

    def __str__(self):
        return 'Stock Name: ' + self.stock_name

    def needs_update(self):
        return self.end_date < timezone.now()

    def how_many_days(self):
        return timezone.now() - self.end_date

class Stock_Owned(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    bought_at = models.IntegerField(default=0)
    bought_on = models.DateTimeField('date bought')
    amount_owned = models.IntegerField(default=0)

    def __str__(self):
        return self.amount_owned.__str__() + ' ' + self.stock.__str__()

class Stock_Day(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    high = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)
    adjustedClose = models.IntegerField(default=0)
    day = models.DateField('Day of Data')

    def __str__(self):
        return self.stock.__str__() + ' ' + self.day.__str__()



