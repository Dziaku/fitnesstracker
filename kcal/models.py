from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    energy_density = models.FloatField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
    ) 

    class Meta:
        ordering = ['name', 'energy_density']

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("kcal:ingredients") 
    
class Meal(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='IngredientQuantity')
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("kcal:meals") 
    
    @property
    def total_meal_energy(self):
        energy = 0
        for ingredient in self.ingredients.all():
            quantity = IngredientQuantity.objects.get(ingredient=ingredient, meal=self).ingredient_quantity / 100
            energy += ingredient.energy_density * quantity
            energy = round(energy, 1) 
        return energy
    
class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient_quantity = models.FloatField(default= 1)
    
class UserLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.meal.name