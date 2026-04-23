from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import(
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView, FormView
)

from . models import Animal
from . forms import AnimalSearchForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'animals/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to the Zoo'
        context['total_animals'] = Animal.objects.count()
        context['captive_count'] = Animal.objects.filter(born_in_captivity=True).count()
        context['wild_count'] = Animal.objects.filter(born_in_captivity=False).count()
        return context
    

class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'
    paginate_by = 5

    def get_queryset(self):
        return Animal.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['page_title'] = 'All animals'
        context['total_count'] = Animal.objects.count()
        return context
    

class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['page_title'] = f'Animal: {animal.name}'
        context['is_elderly'] = animal.age > 15
        context['weight_category'] = self._weight_category(animal.weight)
        return context
    
    @staticmethod
    def _weight_category(weight):
        if weight < 10:
            return 'Small'
        elif weight < 100:
            return 'Medium'
        elif weight < 500:
            return 'Large'
        return 'Very Large'


class AnimalCreateView(CreateView):
    model = Animal
    fields = ['name', 'age', 'weight', 'born_in_captivity']
    template_name = 'animals/animal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add New Animal'
        context['form_action'] = 'Create'
        return context


class AnimalUpdateView(UpdateView):
    model = 'Animal'
    fields = ['name', 'age', 'weight', 'born_in_captivity']
    template_name = 'animals/animal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit: {self.object.name}'
        context['form_action'] = 'Update'
        return context

class AnimalDeleteView(DeleteView):
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animals:animal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete: {self.object.name}'
        return context


class AnimalSearchView(FormView):
    template_name = 'animals/animal_search.html'
    form_class = AnimalSearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.request.GET:
           kwargs['data'] = self.request.GET
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Search Animals'
        context['results'] = None
        context['search_performed'] = False

        form = context['form']
        if self.request.GET and form.is_valid():
            data = form.cleaned_data
            queryset = Animal.objects.all()

            if data.get('name'):
                queryset = queryset.filter(name__icontains=data['name'])
            
            if data.get('min_age') is not None:
                queryset = queryset.filter(age__gte=data['min_age'])
            
            if data.get('max_age')is not None:
                queryset = queryset.filter(age__gte=data['max_age'])
            
            if data.get('min_weight') is not None:
                queryset = queryset.filter(weight__lte=data['min_weight'])
            if data.get('max_weight') is not None:
                queryset = queryset.filter(weight__gte=data['max_weight'])
            
            if data.get('born_in_captivity') is not None:
                queryset =queryset.filter(born_in_captivity=data['born_in_captivity'])
            
            context['results'] = queryset
            context['result_count'] = queryset.count()
            context['search_performed'] = True

        return context

