from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'energy_density']
        help_texts = {
            "energy_density": _("kcal per 100 g"),
        }

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name']

IngredientQuantityFormSet = forms.inlineformset_factory(
    Meal, 
    IngredientQuantity, 
    fields=['ingredient', 'ingredient_quantity'],
    extra=1,  
    can_delete=False
)

IngredientQuantityFormSetWithNoExtra = forms.inlineformset_factory(
    Meal, 
    IngredientQuantity, 
    fields=['ingredient', 'ingredient_quantity'], 
    extra=0,
    can_delete=True
)