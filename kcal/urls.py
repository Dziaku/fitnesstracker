from django.urls import path

from . import views

app_name = 'kcal'
urlpatterns = [
    path('', views.main, name='main-index'),
    path('kcal/', views.KcalIndex.as_view(), name='index'),
    path('kcal/add/', views.AddConsumption.as_view(), name='add-item'),
    path('kcal/edit/<pk>', views.EditConsumption.as_view(), name='edit-item'),
    path('kcal/delete/<pk>', views.DeleteConsumption.as_view(), name='delete-item'),
    path('kcal/meals/', views.MealList.as_view(), name='meals'),
    path('kcal/add/meal', views.AddMeal.as_view(), name='add-meal'),
    path('kcal/meal/edit/<pk>', views.EditMeal.as_view(), name='edit-meal'),
    path('kcal/ingredients/', views.IngredientList.as_view(), name='ingredients'),
    path('kcal/add/ingredient/', views.AddIngredient.as_view(), name='add-ingredient'),
    path('kcal/ingredient/edit/<pk>', views.EditIngredient.as_view(), name='edit-ingredient'),
    path('register/', views.sign_up, name='register')
]