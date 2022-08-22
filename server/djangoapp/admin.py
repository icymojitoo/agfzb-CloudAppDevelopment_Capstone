from django.contrib import admin
# Tabular inline import
from .models import CarMake, CarModel


# Register your models here.
# Please use `root` as user name and `root` as password for your reviewer to login your app.

# CarModelInline
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarMakeAdmin
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name']

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)

