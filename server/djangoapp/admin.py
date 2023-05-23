from django.contrib import admin
from .models import *



class CarModelInline(admin.StackedInline):
    model=CarModel
    extra=4


class CarModelAdmin(admin.ModelAdmin):
    list_display=["dealer_id","car_make", "name", "type", "year"]




class CarMakeAdmin(admin.ModelAdmin):
    model=CarMake
    list_display=["name", 'country']
    inlines=[CarModelInline]



admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
