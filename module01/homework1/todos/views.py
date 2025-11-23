from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Todo

# Create your views here.

class TodoListView(View):
    def get(self, request):
        todos = Todo.objects.all()
        return render(request, 'todos/home.html', {'todos': todos})

class TodoCreateView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')

        if title:
            Todo.objects.create(
                title=title,
                description=description,
                due_date=due_date if due_date else None
            )
        return redirect('todo_list')

class TodoUpdateView(View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.title = request.POST.get('title', todo.title)
        todo.description = request.POST.get('description', todo.description)
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        todo.save()
        return redirect('todo_list')

class TodoDeleteView(View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('todo_list')

class TodoToggleResolvedView(View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.resolved = not todo.resolved
        todo.save()
        return redirect('todo_list')
