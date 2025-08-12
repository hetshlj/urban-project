from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('services-list/', views.services, name='services'),
    path('service-details/', views.servicedetails, name='servicesdetails'),
    path('categories/', views.categories, name='categories'),

]
