from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import *
from django.views import generic
from django.shortcuts import redirect, render

from .models import *
from .forms import *

# GENERAL VIEWS

def main(request):
  return render(request, "main_index.html")

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('kcal:index')
        else:
            return render(request, 'register.html', {'form': form}) 

# KCAL-APP VIEWS

class KcalIndex(LoginRequiredMixin, generic.ListView):
    model = DailyConsumption
    template_name = 'kcal/index.html'

    def get_queryset(self):
       return DailyConsumption.objects.filter(eater=self.request.user)
    
class DailyConsumptionDetail(LoginRequiredMixin, generic.DetailView):
    model = DailyConsumption
    template_name = 'kcal/dailyconsumption_detail.html'

class AddDay(LoginRequiredMixin, generic.CreateView):
   model = DailyConsumption
   fields = ['date', 'meals']
   template_name = 'kcal/generic_form.html'
   
   def form_valid(self, form):    
    form.instance.eater = self.request.user
    return super(AddDay, self).form_valid(form)
   
class EditDay(LoginRequiredMixin,generic.UpdateView):
   model = DailyConsumption
   fields = ['date', 'meals']
   template_name = 'kcal/generic_form.html'
   
   def form_valid(self, form):    
    form.instance.eater = self.request.user
    return super(EditDay, self).form_valid(form)

class MealList(generic.ListView):
   model = Meal

class AddMeal(LoginRequiredMixin, generic.CreateView):
   model = Meal
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'ingredients']
    
   def form_valid(self, form):
    form.instance.author = self.request.user
    return super(AddMeal, self).form_valid(form)

class EditMeal(LoginRequiredMixin, generic.UpdateView):
   model = Meal
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'ingredients']

class IngredientList(generic.ListView):
   model = Ingredient

class IngredientDetail(generic.DetailView):
   model = Ingredient

class AddIngredient(LoginRequiredMixin, generic.CreateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'energy_density']

   def form_valid(self, form):
    form.instance.author = self.request.user
    return super(AddIngredient, self).form_valid(form)
   
class EditIngredient(LoginRequiredMixin, generic.UpdateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'energy_density']

   def form_valid(self, form):
    form.instance.author = self.request.user
    return super(EditIngredient, self).form_valid(form)

   

  

