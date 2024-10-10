from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import *
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views import generic

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
# UserLog CRUD

class KcalIndex(LoginRequiredMixin, generic.ListView):
    model = UserLog
    template_name = 'kcal/index.html'
    context_object_name = 'user_logs'  # Optional: for better readability in the template

    def get_queryset(self):
        # Get the date from the query parameters or default to today
        date_str = self.request.GET.get('date')
        
        if date_str:
            # Try to parse the date from the query parameter
            filter_date = parse_date(date_str)
            if not filter_date:
                filter_date = timezone.localdate()  # Fallback to today if parsing fails
        else:
            filter_date = timezone.localdate()  # Default to today's date if no query parameter
        
        # Filter UserLog by the user and date
        return UserLog.objects.filter(user=self.request.user, date__date=filter_date).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the date from the query parameters or default to today
        date_str = self.request.GET.get('date')
        if date_str:
            current_date = parse_date(date_str)
            if not current_date:
                current_date = timezone.localdate()  # Fallback to today if parsing fails
        else:
            current_date = timezone.localdate()  # Default to today's date if no query parameter

        context['current_date'] = current_date  # Add the current_date to the context
        return context
    
class AddConsumption(LoginRequiredMixin, generic.CreateView):
    model = UserLog
    template_name = 'kcal/generic_form.html'
    fields = ['date', 'meal']
    success_url= reverse_lazy('kcal:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddConsumption, self).form_valid(form)
    
class EditConsumption(LoginRequiredMixin, generic.UpdateView):
    model = UserLog
    template_name = 'kcal/generic_form.html'
    fields = ['date', 'meal']
    success_url= reverse_lazy('kcal:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditConsumption, self).form_valid(form)
    
class DeleteConsumption(LoginRequiredMixin, generic.DeleteView):
    model = UserLog
    success_url= reverse_lazy('kcal:index')

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

   

  

