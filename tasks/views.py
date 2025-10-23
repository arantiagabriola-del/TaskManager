from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Task, Category
from .forms import CustomUserCreationForm
import random


# 🏠 Public Welcome Page
def welcome(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'pages/welcome.html')


# ℹ️ About Page
def about(request):
    return render(request, 'pages/about.html')


# ✅ User Registration
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


# ✅ Dashboard (with productivity stats)
@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())

    # ✅ Counts
    completed_count = Task.objects.filter(user=user, status='COMPLETED').count()
    pending_count = Task.objects.filter(user=user, status='PENDING').count()
    total_tasks = Task.objects.filter(user=user).count()

    # ✅ Productivity summary
    tasks_completed_today = Task.objects.filter(
        user=user,
        status='COMPLETED',
        completed_at__date=today
    ).count()

    tasks_completed_week = Task.objects.filter(
        user=user,
        status='COMPLETED',
        completed_at__date__gte=week_start
    ).count()

    overdue_tasks = Task.objects.filter(
        user=user,
        status='PENDING',
        due_date__lt=today
    ).count()

    avg_focus_time = 45  # placeholder for future tracking feature

    # ✅ Motivational message
    quotes = [
        "Keep pushing, you're doing great!",
        "Small steps lead to big results.",
        "Focus on progress, not perfection.",
        "Your future self will thank you for today’s effort!",
        "You got this! One task at a time.",
        "Every small victory counts!",
        "Discipline beats motivation — keep going!",
    ]
    motivational_message = random.choice(quotes)

    # ✅ Order tasks by priority and due date
    priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    tasks = sorted(
        Task.objects.filter(user=user),
        key=lambda t: (priority_order.get(t.priority, 4), t.due_date or today)
    )

    # 🚨 NEW: Reminders (tasks due in next 24 hours)
    tomorrow = today + timedelta(days=1)
    reminders = Task.objects.filter(
        user=user,
        status='PENDING',
        due_date__gte=today,
        due_date__lte=tomorrow
    ).order_by('due_date')

    # 🔔 NEW: Notifications
    recent_completed = Task.objects.filter(
        user=user,
        status='COMPLETED',
        completed_at__gte=timezone.now() - timedelta(days=1)
    )
    notifications = []

    if overdue_tasks > 0:
        notifications.append(f"You have {overdue_tasks} overdue task(s).")
    if reminders.exists():
        notifications.append(f"You have {reminders.count()} task(s) due soon.")
    if recent_completed.exists():
        notifications.append(f"Great job! You completed {recent_completed.count()} task(s) recently!")

    context = {
        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_tasks': total_tasks,
        'tasks_completed_today': tasks_completed_today,
        'tasks_completed_week': tasks_completed_week,
        'overdue_tasks': overdue_tasks,
        'avg_focus_time': avg_focus_time,
        'motivational_message': motivational_message,
        'tasks': tasks,
        'reminders': reminders,  # 👈 new
        'notifications': notifications,  # 👈 new
    }

    return render(request, 'tasks/dashboard.html', context)


# ✅ Focus Mode – Pending Tasks Sorted by Priority & Due Date
@login_required
def task_list(request):
    pending_tasks = Task.objects.filter(
        user=request.user, status='PENDING'
    ).order_by('-priority', 'due_date')

    context = {'pending_tasks': pending_tasks}
    return render(request, 'tasks/task_list.html', context)


# ✅ Task Create
@login_required
def task_create(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date', None)
        priority = request.POST.get('priority', 'MEDIUM')
        new_category_name = request.POST.get('new_category', '').strip()

        task = Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date,
            status='PENDING',
            priority=priority,
            created_at=timezone.now()
        )

        selected_categories = request.POST.getlist('categories')
        if selected_categories:
            task.categories.set(selected_categories)

        if new_category_name:
            new_cat, _ = Category.objects.get_or_create(
                user=request.user,
                title=new_category_name
            )
            task.categories.add(new_cat)

        return redirect('dashboard')

    return render(request, 'tasks/task_form.html', {'categories': categories})


# ✅ Task Update
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.due_date = request.POST.get('due_date', None)
        task.priority = request.POST.get('priority', 'MEDIUM')
        task.save()

        selected_categories = request.POST.getlist('categories')
        task.categories.set(selected_categories)

        return redirect('dashboard')

    return render(request, 'tasks/task_form.html', {'task': task, 'categories': categories})


# ✅ Task Delete
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('dashboard')


# ✅ Mark Task as Complete
@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'COMPLETED'
    task.completed_at = timezone.now()
    task.save()
    return redirect('dashboard')
