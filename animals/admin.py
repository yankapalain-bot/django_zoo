from django.contrib import admin
from . models import Animal

# Register your models here.
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'wight', 'born_in_captivity']
    list_filter = ['born_in_captivity']
    search_fields = ['name']
