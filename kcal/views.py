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

## KCAL-APP VIEWS
# DailyConsumption CRUD

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

# Meal CRUD

class MealList(generic.ListView):
   model = Meal

class AddMeal(LoginRequiredMixin, generic.CreateView):
    model = Meal
    form_class = MealForm
    
    def get_context_data(self, **kwargs):
        """Pass the formset to the template."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_quantity_formset'] = IngredientQuantityFormSet(self.request.POST)
        else:
            context['ingredient_quantity_formset'] = IngredientQuantityFormSet()
        return context

    def form_valid(self, form):
        """Handle saving the Meal and its associated IngredientQuantities."""
        context = self.get_context_data()
        ingredient_quantity_formset = context['ingredient_quantity_formset']

        if ingredient_quantity_formset.is_valid():
            # Save the Meal instance first
            meal = form.save(commit=False)
            meal.author = self.request.user  # Set the current user as the author
            meal.save()

            # Save the IngredientQuantity formset
            ingredient_quantities = ingredient_quantity_formset.save(commit=False)
            for ingredient_quantity in ingredient_quantities:
                ingredient_quantity.meal = meal  # Associate with the saved meal
                ingredient_quantity.save()

            return redirect(meal.get_absolute_url())  # Redirect to the detail view of the created meal

        else:
            # If formset is not valid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form))

class EditMeal(LoginRequiredMixin, generic.UpdateView):
    model = Meal
    form_class = MealForm
    
    def get_context_data(self, **kwargs):
        """Pass the formset to the template."""
        context = super().get_context_data(**kwargs)
        meal = self.object
        if self.request.POST:
            context['ingredient_quantity_formset'] = IngredientQuantityFormSetWithNoExtra(self.request.POST, instance=meal)
        else:
            context['ingredient_quantity_formset'] = IngredientQuantityFormSetWithNoExtra(instance=meal)
        return context

    def form_valid(self, form):
        """Handle saving the Meal and its associated IngredientQuantities."""
        context = self.get_context_data()
        ingredient_quantity_formset = context['ingredient_quantity_formset']

        if ingredient_quantity_formset.is_valid():
            # Save the Meal instance first
            meal = form.save(commit=False)
            meal.author = self.request.user  # Set the current user as the author
            meal.save()

            # Save the IngredientQuantity formset
            ingredient_quantities = ingredient_quantity_formset.save(commit=False)
            for ingredient_quantity in ingredient_quantities:
                ingredient_quantity.meal = meal  # Associate with the saved meal
                ingredient_quantity.save()

            return redirect(meal.get_absolute_url())  # Redirect to the detail view of the created meal

        else:
            # If formset is not valid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form))
# Ingredient CRUD

class IngredientList(generic.ListView):
   model = Ingredient

class IngredientDetail(generic.DetailView):
   model = Ingredient

class AddIngredient(LoginRequiredMixin, generic.CreateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   form_class = IngredientForm

   def form_valid(self, form):
    form.instance.author = self.request.user
    return super(AddIngredient, self).form_valid(form)
   
class EditIngredient(LoginRequiredMixin, generic.UpdateView):
   model = Ingredient
   template_name = 'kcal/generic_form.html'
   form_class = IngredientForm

   def form_valid(self, form):
    form.instance.author = self.request.user
    return super(EditIngredient, self).form_valid(form)

   

  

