from django.shortcuts import render,redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomUserCreationForm
from django.contrib.auth import login,logout

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, UpdateView

from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# Create your views here.

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


@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

@method_decorator(never_cache, name='dispatch')
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

    
     
@method_decorator(never_cache, name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = 'login'


@method_decorator(never_cache, name='dispatch')
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'

    # fetching from self user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)
        context["count"] = context["tasks"].filter(complete = False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__istartswith = search_input)

        context['search_input'] = search_input
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Prevent showing cached page after logout
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


    
@method_decorator(never_cache, name='dispatch')
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'title'
    
@method_decorator(never_cache, name='dispatch')
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

@method_decorator(never_cache, name='dispatch')
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')


@method_decorator(never_cache, name='dispatch')
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task_confirm_delete.html'


@method_decorator(never_cache, name='dispatch')
class AdminLoginView(LoginView):
    template_name = 'admin_login.html'

    def form_valid(self, form):
        """Runs when username/password are correct."""
        user = form.get_user()
        if user.is_staff or user.is_superuser:
            return super().form_valid(form)
        else:
            messages.error(self.request, "Access denied: Only admins can access this page.")
            logout(self.request)
            return redirect('admin-login')

    def form_invalid(self, form):
        """Runs when username/password are wrong."""
        messages.error(self.request, "Invalid username or password!")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('admin-dashboard')
    
@method_decorator(never_cache, name='dispatch')
class AdminRegisterUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'  # reuse register page
    success_url = reverse_lazy('admin-dashboard')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Admin access required.")
        return redirect('admin-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        messages.success(self.request, f"User '{user.username}' created successfully.")
        return super().form_valid(form)





@method_decorator(never_cache, name='dispatch')
class AdminLogoutView(LogoutView):
    next_page = 'admin-login'


@method_decorator(never_cache, name='dispatch')
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Admin access required.")
        return redirect('admin-login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-is_active')
        return context



@method_decorator(never_cache, name='dispatch')
class AdminUserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'admin_user_edit.html'
    success_url = reverse_lazy('admin-dashboard')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Admin access required.")
        return redirect('admin-login')
