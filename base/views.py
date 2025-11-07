from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.

class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'title'
     