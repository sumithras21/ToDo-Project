from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('update/<int:id>/', views.update_task, name='update_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('add_subtask/<int:task_id>/', views.add_subtask, name='add_subtask'),
    path('update_subtask/<int:id>/', views.update_subtask, name='update_subtask'),
    path('delete_subtask/<int:id>/', views.delete_subtask, name='delete_subtask'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('api/', include(router.urls)),
]