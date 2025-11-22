from django.urls import path
from . import views

urlpatterns = [
    # User Paths
    path('login/', views.custom_login_view, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.custom_logout_view, name="logout"),
    path('', views.task_list, name="tasks"),
    path('task/<int:pk>/', views.task_detail, name="task"), 
    path('task-create/', views.task_create, name="task-create"),
    path('task-update/<int:pk>/', views.task_update, name="task-update"),
    path('task-delete/<int:pk>/', views.task_delete, name="task-delete"),

    # Admin Paths
    path('admin/', views.admin_login_view, name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-user/<int:pk>/edit/', views.admin_user_edit_view, name='admin-user-edit'),
    path('admin-logout/', views.admin_logout_view, name='admin-logout'),
    path('toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle-user-status'),
    path('admin-register-user/', views.admin_register_user_view, name='admin-register-user'),
]