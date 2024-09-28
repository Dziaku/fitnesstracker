from django.urls import path

from . import views

app_name = "kcal"
urlpatterns = [
    path("", views.main, name="main-index"),
    path("kcal/", views.KcalIndex.as_view(), name="index"),
    path('kcal/day/<pk>', views.DailyConsumptionDetail.as_view(), name="day"),
    path('kcal/meal/', views.MealList.as_view(), name="meals"),
    path('kcal/add/meal', views.AddMeal.as_view(), name="add-meal"),
    path('kcal/meal/<pk>', views.MealDetail.as_view(), name="meal-detail"),
    path('kcal/meal/edit/<pk>', views.EditMeal.as_view(), name="edit-meal"),
    path('kcal/ingredient/', views.IngredientList.as_view(), name="ingredients"),
    path('kcal/ingredient/<pk>', views.IngredientDetail.as_view(), name="ingredient-detail"),
    path('kcal/ingredient/add', views.AddIngredient.as_view(), name="add-ingredient"),
    path('kcal/ingredient/edit/<pk>', views.EditIngredient.as_view(), name="edit-ingredient"),
]