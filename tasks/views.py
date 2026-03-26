from django.shortcuts import render, redirect
from .models import Tasks, SubTask
from .forms import Taskform, SubTaskform
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    # show tasks created OR assigned
    tasks = Tasks.objects.filter(
        Q(user=request.user) | Q(assigned_to=request.user)
    )
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = Taskform(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user   # creator
            task.save()
            return redirect('task_list')
    else:
        form = Taskform(user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def update_task(request, id):
    task = Tasks.objects.get(id=id)

    if request.method == 'POST':
        form = Taskform(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = Taskform(instance=task, user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, id):
    task = Tasks.objects.get(id=id)
    task.delete()
    return redirect('task_list')

@login_required
def add_subtask(request, task_id):
    task = Tasks.objects.get(id=task_id)

    if request.method == 'POST':
        form = SubTaskform(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return redirect('task_list')
    else:
        form = SubTaskform()

    return render(request, 'tasks/subtask_form.html', {'form': form})

@login_required
def update_subtask(request, id):
    subtask = SubTask.objects.get(id=id)

    if request.method == 'POST':
        form = SubTaskform(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = SubTaskform(instance=subtask)

    return render(request, 'tasks/subtask_form.html', {'form': form})

@login_required
def delete_subtask(request, id):
    subtask = SubTask.objects.get(id=id)
    subtask.delete()
    return redirect('task_list')

@api_view(['POST'])
def api_create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        # set creator automatically
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['GET'])
def api_get_tasks(request):
    # show tasks created OR assigned
    tasks = Tasks.objects.filter(
        Q(user=request.user) | Q(assigned_to=request.user)
    )
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(
            Q(user=user) | Q(assigned_to=user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)