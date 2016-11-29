from django.contrib import admin

from .models import Stock, User, Portfolio

admin.site.register(Stock)
admin.site.register(Portfolio)