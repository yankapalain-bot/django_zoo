from django.db import models
from django.urls import reverse

# Create your models here.
class Animal(models.Model):
    name=               models.CharField(max_length=100)
    age=                models.IntegerField(help_text="Age in years")
    weight=             models.FloatField(help_text="Weight in kilograms")
    born_in_captivity=  models.BooleanField(default=False)

    class Meta:
        ordering = ['name']     #Always sorted A-Z
    
    def __str__(self):
        return f"{self.name} (age {self.age})"
    
    def get_absolute_url(self):
        return reverse('animals:animal-detail', kwargs={'pk': self.pk})