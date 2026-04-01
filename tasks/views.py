from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from .forms import Taskform
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TaskSerializer

#authentication
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
            login(request, form.get_user())
            return redirect('task_list')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

#task details
@login_required
def task_list(request):
    tasks = Tasks.objects.filter(
        Q(user=request.user) | Q(assigned_to=request.user),
        parent__isnull=True
    )
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = Taskform(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = Taskform(user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def update_task(request, id):
    task = get_object_or_404(Tasks, id=id)

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
    task = get_object_or_404(Tasks, id=id)
    task.delete()
    return redirect('task_list')

#subtask 
@login_required
def add_subtask(request, task_id):
    parent_task = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST':
        form = Taskform(request.POST, user=request.user, parent=parent_task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = Taskform(user=request.user)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'parent_task': parent_task
    })


@login_required
def update_subtask(request, id):
    subtask = get_object_or_404(Tasks, id=id)

    if request.method == 'POST':
        form = Taskform(request.POST, instance=subtask, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = Taskform(instance=subtask, user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def delete_subtask(request, id):
    subtask = get_object_or_404(Tasks, id=id)
    subtask.delete()
    return redirect('task_list')

#api 

@api_view(['POST'])
def api_create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['GET'])
def api_get_tasks(request):
    tasks = Tasks.objects.filter(
        Q(user=request.user) | Q(assigned_to=request.user),
        parent__isnull=True
    )
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

#viewset
from rest_framework import filters

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter  
    ]

    filterset_fields = ['title', 'description', 'completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']  

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(
            Q(user=user) | Q(assigned_to=user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#generic view
class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(
            Q(user=user) | Q(assigned_to=user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]