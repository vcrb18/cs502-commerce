from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Auction, User

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'image', 'description', 'date', 'category')



admin.site.register(Auction, AuctionAdmin)
admin.site.register(User)