from django.shortcuts import render,redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, UpdateView

from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args, **kwargs)
    
     

class CustomLogoutView(LogoutView):
    next_page = 'login'



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

    

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'title'
     
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task_confirm_delete.html'


class AdminLoginView(LoginView):
    template_name = 'admin_login.html'

    def get_success_url(self):
        # Allow only staff/superusers
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse_lazy('admin-dashboard')
        messages.error(self.request, "Access Denied: Only Admins can log in here.")
        return reverse_lazy('login')

# ✅ Admin Logout View
class AdminLogoutView(LogoutView):
    next_page = 'admin-login'


# ✅ Admin Dashboard (only admin can access)
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Admin access required.")
        return redirect('admin-login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


# ✅ Edit User (only admin)
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
