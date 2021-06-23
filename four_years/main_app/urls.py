from django.contrib import admin
from django.urls import path
from . import views

"""
В этом файле мы описываем url адреса, и какие представления вызывать при обращении к ним. 
"""

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('application/', views.ApplicationView.as_view(), name='application'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', views.logout, name='logout'),
    path('get_spec/', views.get_specializations, name='get_spec'),
]