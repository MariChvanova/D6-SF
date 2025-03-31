from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.subscriptions, name='subscriptions'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),

]


