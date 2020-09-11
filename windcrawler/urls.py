from django.contrib import admin
from django.urls import path
from windcrawler_app import views

urlpatterns = [
    path('no-admin-allowed/', admin.site.urls),
    path('trigger/', views.trigger, name='trigger'),
    path('', views.home, name='home'),
] 
