from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy

# Create your views here.

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
    success_url = reverse_lazy('task')
    template_name = 'task_form.html'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_form.html'
    success_url = reverse_lazy('task')