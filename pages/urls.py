from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),  # public landing page
    path('home/', views.home, name='home'),          # authenticated users' home
    path('about/', views.about, name='about'),
]
