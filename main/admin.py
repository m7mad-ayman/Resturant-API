from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Table)
admin.site.register(Ingredient)
admin.site.register(Reservation)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(OrderItem)



