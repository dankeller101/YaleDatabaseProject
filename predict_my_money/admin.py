from django.contrib import admin

from .models import Stock, User, Portfolio, Stock_Day, Portfolio_Day

admin.site.register(Stock)
admin.site.register(Stock_Day)
admin.site.register(Portfolio)
admin.site.register(Portfolio_Day)