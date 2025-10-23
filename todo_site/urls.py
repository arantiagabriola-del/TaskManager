"""
URL configuration for todo_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Root redirect: show welcome page or dashboard based on login
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')  # logged-in users go to dashboard
    return redirect('welcome')       # visitors go to welcome page

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL logic
    path('', root_redirect, name='root_redirect'),

    # 🌐 Static pages (About, etc.)
    path('pages/', include('pages.urls')),

    # ✅ Task Management & Auth
    path('tasks/', include('tasks.urls')),
]








