from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Player)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(RoomItem)