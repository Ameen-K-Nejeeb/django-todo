from django.urls import path
from .views import (
    TaskList, TaskDetail, TaskCreate, TaskUpdate, RegisterPage,
    TaskDelete, CustomLoginView, CustomLogoutView
)# from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',CustomLoginView.as_view(), name = "login"),
    path('register/',RegisterPage.as_view(), name = "register"),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('',TaskList.as_view(), name = "tasks"),
    path('task/<int:pk>/',TaskDetail.as_view(),name = "task"), 
    path('task-create/',TaskCreate.as_view(),name = "task-create"),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name = "task-update"),
    path('task-delete/<int:pk>/',TaskDelete.as_view(), name = "task-delete"),

]