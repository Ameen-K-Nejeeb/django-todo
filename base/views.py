from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'title'
     
class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'
