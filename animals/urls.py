from django.urls import path
from . import views

app_name = 'animals'   # Enables URL namespacing (e.g., {% url 'animals:animal-list' %})

urlpatterns = [
    # TemplateView: Home page
    path('', views.HomeView.as_view(), name='home'),

    # ListView: All animals
    path('animals/', views.AnimalListView.as_view(), name='animal-list'),

    # DetailView: Single animal
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(), name='animal-detail'),

    # CreateView: Add new animal
    path('animals/add/', views.AnimalCreateView.as_view(), name='animal-create'),

    # UpdateView: Edit existing animal
    path('animals/<int:pk>/edit/', views.AnimalUpdateView.as_view(), name='animal-update'),

    # DeleteView: Delete animal
    path('animals/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),

    # FormView: Search animals
    path('animals/search/', views.AnimalSearchView.as_view(), name='animal-search'),
]