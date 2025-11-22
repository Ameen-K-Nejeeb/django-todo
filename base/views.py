from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Task
from .forms import CustomUserCreationForm, TaskForm, UserEditForm
from django.db.models import Q

# --- Helper Function for Admin Check ---
def is_admin(user):
    return user.is_staff or user.is_superuser

# --- User Views ---

@never_cache
def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@never_cache
def register_page(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@never_cache
def custom_logout_view(request):
    logout(request)
    return redirect('login')

@never_cache
@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    count = tasks.filter(complete=False).count()

    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-dashboard')

    search_input = request.GET.get('search-area') or ''
    if search_input:
        tasks = tasks.filter(title__istartswith=search_input)

    context = {
        'tasks': tasks,
        'count': count,
        'search_input': search_input
    }
    return render(request, 'task_list.html', context)

@never_cache
@login_required(login_url='login')
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'title': task})



@login_required(login_url='login')
@never_cache
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
        
    return render(request, 'task_form.html', {'form': form})



@never_cache
@login_required(login_url='login')
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
        
    return render(request, 'task_form.html', {'form': form})




@never_cache
@login_required(login_url='login')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
        
    return render(request, 'task_confirm_delete.html', {'task': task})





# --- Admin Views ---

@never_cache
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_admin(user):
                login(request, user)
                return redirect('admin-dashboard')
            else:
                messages.error(request, "Access denied: Only admins can access this page.")
                # Don't login non-admins here
        else:
            messages.error(request, "Invalid username or password!")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})



@never_cache
@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def admin_dashboard_view(request):
    users = User.objects.all().order_by('-is_active')

    search_query = request.GET.get('search_query')
    if search_query:
        users = users.filter( Q(username__icontains=search_query) | Q(email__icontains=search_query))

    context = {
        'users':users,
        'search_query': search_query if search_query else ''
    }

    return render(request, 'admin_dashboard.html', context)



@never_cache
@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def admin_register_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, f"User '{user.username}' created successfully.")
            return redirect('admin-dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})



@never_cache
@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def admin_user_edit_view(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = UserEditForm(instance=user_obj)
        
    return render(request, 'admin_user_edit.html', {'form': form})



@never_cache
def admin_logout_view(request):
    logout(request)
    return redirect('admin-login')



# This one was already an FBV, keeping it as is
@never_cache
@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        messages.error(request, f"{user.username} has been deactivated.")
    else:
        user.is_active = True
        messages.success(request, f"{user.username} has been reactivated.")
    user.save()
    return redirect('admin-dashboard')