from django.urls import path

from . import views

app_name = 'kcal'
urlpatterns = [
    path('', views.main, name='main-index'),
    path('kcal/', views.KcalIndex.as_view(), name='index'),
    path('kcal/day/<pk>', views.DailyConsumptionDetail.as_view(), name='day'),
    path('kcal/add/day', views.AddDay.as_view(), name='add-day'),
    path('kcal/edit/day/<pk>', views.EditDay.as_view(), name='edit-day'),
    path('kcal/meals/', views.MealList.as_view(), name='meals'),
    path('kcal/add/meal', views.AddMeal.as_view(), name='add-meal'),
    path('kcal/meal/edit/<pk>', views.EditMeal.as_view(), name='edit-meal'),
    path('kcal/ingredients/', views.IngredientList.as_view(), name='ingredients'),
    path('kcal/add/ingredient/', views.AddIngredient.as_view(), name='add-ingredient'),
    path('kcal/ingredient/edit/<pk>', views.EditIngredient.as_view(), name='edit-ingredient'),
    path('register/', views.sign_up, name='register')
]