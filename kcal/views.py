from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse
from django.template import loader

from .models import *

def main(request):
  template = loader.get_template('main_index.html')
  return HttpResponse(template.render())

class KcalIndex(LoginRequiredMixin, generic.ListView):
    model = DailyConsumption
    template_name = 'kcal/index.html'
    login_url = '/login/'
    redirect_field_name = "redirect_to"

    def get_queryset(self):
       return DailyConsumption.objects.filter(eater=self.request.user)
    
class DailyConsumptionDetail(LoginRequiredMixin, generic.DetailView):
    model = DailyConsumption
    template_name = 'kcal/dailyconsumption_detail.html'
    login_url = '/login/'
    redirect_field_name = "redirect_to"

    def get_queryset(self):
       return DailyConsumption.objects.filter(eater=self.request.user)

class MealList(generic.ListView):
   model = Meal

class MealDetail(generic.DetailView):
   model = Meal

class AddMeal(LoginRequiredMixin, generic.CreateView):
   model = Meal
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'ingredients']
   login_url = '/login/'
   redirect_field_name = "redirect_to"

class EditMeal(LoginRequiredMixin, generic.UpdateView):
   model = Meal
   template_name = 'kcal/generic_form.html'
   fields = ['name', 'ingredients']
   login_url = '/login/'
   redirect_field_name = "redirect_to"

class IngredientList(generic.ListView):
   model = Ingredient

class IngredientDetail(generic.DetailView):
   model = Ingredient

class AddIngredient(LoginRequiredMixin, generic.CreateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   login_url = '/login/'
   redirect_field_name = "redirect_to"

class EditIngredient(LoginRequiredMixin, generic.UpdateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   login_url = 'accounts/login/'
   redirect_field_name = "redirect_to"
  

