from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    return render(request, 'task_list.html', {'tasks': Task.objects.all()})


def task_form(request, pk=None):
    """Handles BOTH create (pk=None) and update (pk given)."""
    task = get_object_or_404(Task, pk=pk) if pk else None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!' if task else 'Task created!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form, 'task': task})


@require_POST
def task_delete(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    messages.success(request, 'Task deleted.')
    return redirect('task_list')