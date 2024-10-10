from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class IngredientInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 3

class MealAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ['name', 'total_meal_energy']

class UserLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'meal', 'user']

admin.site.register(UserLog, UserLogAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient)
