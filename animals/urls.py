from django.urls import path
from . import views

app_name = 'animals'   #Enables URL namespacing(e.g, {% url 'animals:animal-list' %})

urlpatterns = [
    #TemplateView: Home page
    path('', views.HomeView.as_view(), name='home'),
]