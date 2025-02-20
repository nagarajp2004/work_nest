from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.http import HttpResponseForbidden


  # Render the home page

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def task_list(request):
    # Fetch tasks created by the logged-in user
    created_tasks = Task.objects.filter(created_by=request.user)
    
    # Fetch tasks assigned to the logged-in user
    assigned_tasks = Task.objects.filter(assigned_to=request.user)
    
    return render(request, 'task_list.html', {
        'created_tasks': created_tasks,
        'assigned_tasks': assigned_tasks,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user  # Set the current user as the creator
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Check if the current user is the creator
    if task.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('task_list')  # Redirect if the user is not the creator

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if the current user is the creator
    if task.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('task_list')  # Redirect if the user is not the creator

    if request.method == 'POST':
        # If it's a POST request, delete the task
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')

    # For GET requests, show the confirmation page
    return render(request, 'task_confirm_delete.html', {'task': task})

# myapp/views.py
from rest_framework import viewsets
from .models import Task
from .serializers import Taskserializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = Taskserializer
