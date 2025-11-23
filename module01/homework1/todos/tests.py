from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo
from datetime import date

# Create your tests here.

class TodoModelTests(TestCase):
    def test_create_todo(self):
        """Test creating a TODO item"""
        todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date(2025, 12, 31)
        )
        self.assertEqual(todo.title, "Test TODO")
        self.assertEqual(todo.description, "Test description")
        self.assertEqual(todo.due_date, date(2025, 12, 31))
        self.assertFalse(todo.resolved)

    def test_todo_string_representation(self):
        """Test the string representation of TODO"""
        todo = Todo.objects.create(title="Test TODO")
        self.assertEqual(str(todo), "Test TODO")

    def test_todo_default_resolved_status(self):
        """Test that new TODOs are not resolved by default"""
        todo = Todo.objects.create(title="Test TODO")
        self.assertFalse(todo.resolved)

class TodoViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_todo_list_view(self):
        """Test the TODO list view displays correctly"""
        Todo.objects.create(title="Test TODO 1")
        Todo.objects.create(title="Test TODO 2")

        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test TODO 1")
        self.assertContains(response, "Test TODO 2")

    def test_create_todo_view(self):
        """Test creating a TODO via POST request"""
        response = self.client.post(reverse('todo_create'), {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New TODO')
        self.assertEqual(todo.description, 'New description')

    def test_create_todo_without_optional_fields(self):
        """Test creating a TODO without description and due date"""
        response = self.client.post(reverse('todo_create'), {
            'title': 'Simple TODO'
        })
        self.assertEqual(response.status_code, 302)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Simple TODO')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)

    def test_update_todo_view(self):
        """Test updating a TODO"""
        todo = Todo.objects.create(title="Original Title")
        response = self.client.post(reverse('todo_update', args=[todo.pk]), {
            'title': 'Updated Title',
            'description': 'Updated description',
            'due_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Title')
        self.assertEqual(todo.description, 'Updated description')

    def test_delete_todo_view(self):
        """Test deleting a TODO"""
        todo = Todo.objects.create(title="To Be Deleted")
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.post(reverse('todo_delete', args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle_resolved_view(self):
        """Test toggling the resolved status of a TODO"""
        todo = Todo.objects.create(title="Test TODO", resolved=False)

        # Toggle to resolved
        response = self.client.post(reverse('todo_toggle', args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)

        # Toggle back to unresolved
        response = self.client.post(reverse('todo_toggle', args=[todo.pk]))
        todo.refresh_from_db()
        self.assertFalse(todo.resolved)

    def test_todo_list_ordering(self):
        """Test that TODOs are ordered by creation date (newest first)"""
        todo1 = Todo.objects.create(title="First TODO")
        todo2 = Todo.objects.create(title="Second TODO")

        response = self.client.get(reverse('todo_list'))
        todos = response.context['todos']
        self.assertEqual(todos[0].title, "Second TODO")
        self.assertEqual(todos[1].title, "First TODO")

    def test_get_nonexistent_todo(self):
        """Test accessing a TODO that doesn't exist"""
        response = self.client.post(reverse('todo_delete', args=[999]))
        self.assertEqual(response.status_code, 404)
