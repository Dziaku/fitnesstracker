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
            quantity = IngredientQuantity.objects.get(ingredient=ingredient, meal=self).ingredient_quantity
            energy += ingredient.energy_density * quantity 
        return energy

    
class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient_quantity = models.FloatField()
    
class DailyConsumption(models.Model):
    date = models.DateField(default=timezone.now)
    meals = models.ManyToManyField(Meal, through='MealQuantity')
    eater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('date','eater'),)

    def __str__(self) -> str:
        return f'{self.eater} consumed {self.total_day_energy}'
    
    @property
    def total_day_energy(self):
        energy = 0
        for meal in self.meals.all():
            quantity = MealQuantity.objects.get(meal=meal, day=self).meal_quantity
            energy += meal.total_meal_energy*quantity
        return energy

class MealQuantity(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day = models.ForeignKey(DailyConsumption, on_delete=models.CASCADE)
    meal_quantity = models.IntegerField(default=1, choices=((i,i) for i in range(1, 101)))