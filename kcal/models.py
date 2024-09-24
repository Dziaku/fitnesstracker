from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    energy_density = models.FloatField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
    ) 

    def __str__(self) -> str:
        return self.name
    
class Meal(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='IngredientQuantity')
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
    
    def get_meal_energy(self):
        energy = 0
        for ingredient in self.ingredients.all():
            ingredientquantity = IngredientQuantity.objects.get(ingredient=ingredient, meal=self)
            energy += ingredient.energy_density * ingredientquantity.ingredient_quantity 
        return energy

    
class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient_quantity = models.FloatField()

    def __str__(self):
        return "{}_{}:{}".format(self.meal.__str__(), self.ingredient.__str__(), self.ingredient_quantity)