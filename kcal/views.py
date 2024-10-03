from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import *

def main(request):
  return render(request, "main_index.html")

class KcalIndex(LoginRequiredMixin, generic.ListView):
    model = DailyConsumption
    template_name = 'kcal/index.html'

    def get_queryset(self):
       return DailyConsumption.objects.filter(eater=self.request.user)
    
class DailyConsumptionDetail(LoginRequiredMixin, generic.DetailView):
    model = DailyConsumption
    template_name = 'kcal/dailyconsumption_detail.html'

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

  

