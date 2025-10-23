from django.shortcuts import render, redirect

# 🏠 Public Welcome Page
def welcome(request):
    """Landing page accessible to everyone."""
    if request.user.is_authenticated:
        return redirect('task_list')  # Redirect logged-in users to dashboard
    return render(request, 'pages/welcome.html')


def home(request):
    return render(request, 'pages/home.html')


def about(request):
    return render(request, 'pages/about.html')
