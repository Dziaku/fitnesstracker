from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Meal, Ingredient

admin.site.register(User, UserAdmin)
admin.site.register(Meal)
admin.site.register(Ingredient)