from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class IngredientInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 3

class MealInline(admin.TabularInline):
    model = MealQuantity
    extra = 3

class MealAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ['name', 'total_meal_energy']

class DailyConsumptionAdmin(admin.ModelAdmin):
    inlines = [MealInline]
    list_display = ['date', 'eater', 'total_day_energy']
    list_filter = ['date', 'eater']
    search_fields = ['date', 'eater']

admin.site.register(DailyConsumption, DailyConsumptionAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient)
