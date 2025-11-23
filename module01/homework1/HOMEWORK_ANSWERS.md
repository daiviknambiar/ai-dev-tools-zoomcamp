# Homework 1 - Django TODO Application Answers

## Question 1: Install Django

**Question:** What's the command you used to install Django?

**Answer:** `uv pip install django`

### Details:
- We used `uv` as the package manager (as requested in the homework)
- First created a virtual environment with `uv venv`
- Then installed Django with `uv pip install django`
- Django version installed: 5.2.8

---

## Question 2: Project and App

**Question:** What's the file you need to edit to include the app in the project?

**Answer:** `settings.py`

### Details:
- Created project with: `django-admin startproject todoproject .`
- Created app with: `python manage.py startapp todos`
- Edited `todoproject/settings.py` to add `'todos'` to the `INSTALLED_APPS` list
- This registers the app with Django so it can find models, templates, and other app components

**File modified:** `todoproject/settings.py` (lines 33-41)

---

## Question 3: Django Models

**Question:** What's the next step you need to take after creating models?

**Answer:** Run migrations

### Details:
We created a `Todo` model with the following fields:
- `title` - CharField (required)
- `description` - TextField (optional)
- `due_date` - DateField (optional)
- `resolved` - BooleanField (default: False)
- `created_at` - DateTimeField (auto)
- `updated_at` - DateTimeField (auto)

After creating the model, we ran:
1. `python manage.py makemigrations` - Creates migration files
2. `python manage.py migrate` - Applies migrations to database

**File created:** `todos/models.py`

---

## Question 4: TODO Logic

**Question:** Where do we put the TODO logic?

**Answer:** `views.py`

### Details:
We implemented the following class-based views in `todos/views.py`:
- `TodoListView` - Display all TODOs (GET)
- `TodoCreateView` - Create new TODOs (POST)
- `TodoUpdateView` - Edit existing TODOs (POST)
- `TodoDeleteView` - Delete TODOs (POST)
- `TodoToggleResolvedView` - Mark TODOs as resolved/unresolved (POST)

We also created URL routing:
- Created `todos/urls.py` with URL patterns
- Updated `todoproject/urls.py` to include the todos URLs

**Files created/modified:**
- `todos/views.py`
- `todos/urls.py` (created)
- `todoproject/urls.py` (modified)

---

## Question 5: Templates

**Question:** Where do you need to register the directory with the templates?

**Answer:** `TEMPLATES['DIRS']` in project's `settings.py`

### Details:
We created two templates:
- `todos/templates/todos/base.html` - Base template with HTML structure and CSS styling
- `todos/templates/todos/home.html` - Home page with TODO list and forms

Django automatically finds templates in app directories when `APP_DIRS: True` is set in `TEMPLATES` configuration. However, if you needed to register a custom templates directory outside of app folders, you would add it to `TEMPLATES['DIRS']` in `settings.py`.

**Configuration in settings.py:**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Custom template directories go here
        'APP_DIRS': True,  # This finds templates in app directories
        ...
    },
]
```

---

## Question 6: Tests

**Question:** What's the command you use for running tests in the terminal?

**Answer:** `python manage.py test`

### Test Scenarios Covered:

#### Model Tests (3 tests):
1. **test_create_todo** - Test creating a TODO with all fields
2. **test_todo_string_representation** - Test the `__str__` method
3. **test_todo_default_resolved_status** - Test default resolved status is False

#### View Tests (8 tests):
4. **test_todo_list_view** - Test list view displays TODOs correctly
5. **test_create_todo_view** - Test creating TODO via POST with all fields
6. **test_create_todo_without_optional_fields** - Test creating TODO with only required fields
7. **test_update_todo_view** - Test updating an existing TODO
8. **test_delete_todo_view** - Test deleting a TODO
9. **test_toggle_resolved_view** - Test toggling resolved status (both ways)
10. **test_todo_list_ordering** - Test TODOs are ordered by creation date (newest first)
11. **test_get_nonexistent_todo** - Test 404 error for non-existent TODO

### Test Results:
```
Found 11 test(s).
Ran 11 tests in 0.026s
OK
```

All 11 tests passed successfully!

**File created:** `todos/tests.py`

---

## Running the Application

To run the application:

```bash
cd homework1
source ../.venv/bin/activate
python manage.py runserver
```

Then visit: http://127.0.0.1:8000/

### Application Features:
- ✅ Create TODOs with title, description, and due date
- ✅ Edit existing TODOs
- ✅ Delete TODOs (with confirmation)
- ✅ Mark TODOs as resolved/unresolved
- ✅ View all TODOs sorted by creation date
- ✅ Clean, responsive UI with CSS styling
- ✅ Form validation
- ✅ CSRF protection
- ✅ Fully tested with 11 passing tests

---

## Summary

This homework successfully demonstrates:
1. Installing Django with `uv`
2. Creating a Django project and app
3. Configuring settings.py to include the app
4. Defining models with appropriate field types
5. Running migrations to create database tables
6. Implementing views with CRUD operations
7. Creating URL routing
8. Building templates with Django template language
9. Writing comprehensive tests
10. Running a working web application
