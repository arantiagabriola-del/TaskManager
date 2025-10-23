from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ✅ Public / Welcome Page
    path('', views.welcome, name='welcome'),              # Root of tasks app
    path('welcome/', views.welcome, name='welcome'),      # Optional alias

    # ✅ Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),  # After logout, redirect to welcome

    # ✅ Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),  # New dedicated dashboard view

    # ✅ Task Management URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', views.task_update, name='task_update'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('tasks/complete/<int:pk>/', views.task_complete, name='task_complete'),
]
