# Django TODO Application - Project Overview

## 📋 Project Description

A fully functional TODO application built with Django that allows users to create, edit, delete, and manage TODO items with due dates and resolution status.

---

## 🏗️ Project Structure

```
homework1/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── HOMEWORK_ANSWERS.md          # Homework questions and answers
├── PROJECT_OVERVIEW.md          # This file
├── todoproject/                 # Django project directory
│   ├── __init__.py
│   ├── settings.py             # Project settings (includes 'todos' app)
│   ├── urls.py                 # Project URL configuration
│   ├── asgi.py
│   └── wsgi.py
└── todos/                       # TODO application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py               # Todo model definition
    ├── views.py                # View logic (CRUD operations)
    ├── urls.py                 # App URL patterns
    ├── tests.py                # Test suite (11 tests)
    ├── migrations/             # Database migrations
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── templates/
        └── todos/
            ├── base.html       # Base template with styling
            └── home.html       # Main TODO list page
```

---

## 🗄️ Database Model

### Todo Model (`todos/models.py`)

| Field        | Type          | Description                          |
|-------------|---------------|--------------------------------------|
| id          | AutoField     | Primary key (auto-generated)         |
| title       | CharField     | TODO title (max 200 chars, required) |
| description | TextField     | Optional description                 |
| due_date    | DateField     | Optional due date                    |
| resolved    | BooleanField  | Resolution status (default: False)   |
| created_at  | DateTimeField | Auto-set on creation                 |
| updated_at  | DateTimeField | Auto-updated on save                 |

**Meta Options:**
- Ordering: `-created_at` (newest first)
- String representation: Returns the title

---

## 🎯 Features Implemented

### CRUD Operations
- ✅ **Create** - Add new TODOs with title, description, and due date
- ✅ **Read** - View all TODOs in a list format
- ✅ **Update** - Edit existing TODOs
- ✅ **Delete** - Remove TODOs with confirmation dialog

### Additional Features
- ✅ **Mark as Resolved** - Toggle TODO resolution status
- ✅ **Due Dates** - Assign optional due dates to TODOs
- ✅ **Timestamps** - Track creation and update times
- ✅ **Ordering** - Display TODOs with newest first
- ✅ **Responsive UI** - Clean interface with CSS styling
- ✅ **Form Validation** - Title required, other fields optional
- ✅ **CSRF Protection** - Security tokens on all forms

---

## 🔄 URL Routes

| URL Pattern        | View                  | Name          | Method | Description           |
|-------------------|-----------------------|---------------|--------|-----------------------|
| `/`               | TodoListView          | todo_list     | GET    | Display all TODOs     |
| `/create/`        | TodoCreateView        | todo_create   | POST   | Create new TODO       |
| `/update/<id>/`   | TodoUpdateView        | todo_update   | POST   | Update TODO           |
| `/delete/<id>/`   | TodoDeleteView        | todo_delete   | POST   | Delete TODO           |
| `/toggle/<id>/`   | TodoToggleResolvedView| todo_toggle   | POST   | Toggle resolved status|

---

## 🎨 Views Architecture

### Class-Based Views

All views inherit from Django's `View` class:

1. **TodoListView**
   - Retrieves all TODOs from database
   - Renders home template with TODO list
   - Uses GET method

2. **TodoCreateView**
   - Accepts title, description, due_date from POST
   - Creates new TODO object
   - Redirects to list view

3. **TodoUpdateView**
   - Gets TODO by primary key
   - Updates fields from POST data
   - Redirects to list view

4. **TodoDeleteView**
   - Gets TODO by primary key
   - Deletes from database
   - Redirects to list view

5. **TodoToggleResolvedView**
   - Gets TODO by primary key
   - Toggles resolved boolean
   - Redirects to list view

---

## 🖼️ Templates

### base.html
- HTML5 boilerplate
- Embedded CSS styling
- Responsive design (max-width: 800px)
- Color-coded buttons (primary, success, danger, secondary)
- Block system for content injection

### home.html
- Extends base.html
- TODO creation form (title, description, due_date)
- TODO list display
- Inline edit forms (hidden by default)
- JavaScript for toggle edit forms
- Action buttons (Resolve/Unresolve, Edit, Delete)
- Visual differentiation for resolved items (opacity + strikethrough)

---

## 🧪 Testing

### Test Suite (`todos/tests.py`)

**Test Coverage:**
- Model creation and defaults
- String representation
- List view rendering
- CRUD operations via POST requests
- Optional vs required fields
- Toggle functionality
- Ordering verification
- 404 error handling

**Commands:**
```bash
# Run all tests
python manage.py test

# Run with verbosity
python manage.py test -v 2

# Run specific test class
python manage.py test todos.tests.TodoModelTests
```

**Results:**
- 11 tests total
- 11 passed
- 0 failures
- Execution time: ~0.026s

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- `uv` package manager

### Installation Steps

1. **Navigate to homework1 directory:**
   ```bash
   cd homework1
   ```

2. **Activate virtual environment:**
   ```bash
   source ../.venv/bin/activate
   ```

3. **Database is already set up** (db.sqlite3 included)

   If you need to recreate it:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - URL: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/ (need to create superuser first)

### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

---

## 🧰 Technology Stack

| Component        | Technology    | Version |
|-----------------|---------------|---------|
| Framework       | Django        | 5.2.8   |
| Language        | Python        | 3.13.9  |
| Database        | SQLite        | 3.x     |
| Package Manager | uv            | latest  |
| Testing         | Django TestCase| Built-in|
| Frontend        | HTML/CSS/JS   | Vanilla |

---

## 📦 Dependencies

Installed via `uv pip install django`:
- **django** (5.2.8) - Web framework
- **asgiref** (3.11.0) - ASGI server support
- **sqlparse** (0.5.3) - SQL parsing utilities

---

## 🔐 Security Features

- ✅ CSRF tokens on all forms
- ✅ SQL injection protection (ORM)
- ✅ XSS protection (template escaping)
- ✅ Confirmation dialog for delete operations
- ✅ Input validation (title required)
- ✅ Database field constraints

---

## 🎓 Key Django Concepts Demonstrated

1. **MVT Architecture** - Models, Views, Templates separation
2. **ORM** - Database abstraction with models
3. **Class-Based Views** - Organized view logic
4. **URL Routing** - Clean URL patterns with reverse lookups
5. **Template Inheritance** - Base template with blocks
6. **Forms & Validation** - POST data handling
7. **Migrations** - Database schema management
8. **Testing** - Comprehensive test coverage
9. **Settings Management** - App configuration
10. **Static Files** - CSS styling (embedded)

---

## 📝 Development Notes

### Design Decisions:

1. **Class-Based Views**: Chose CBVs for better organization and potential for future extension
2. **Embedded CSS**: Kept styling in base.html for simplicity (could be moved to static files)
3. **SQLite**: Used default database for development (easily switchable to PostgreSQL/MySQL)
4. **No Django Forms**: Used raw HTML forms to demonstrate fundamentals
5. **Inline Editing**: JavaScript-based inline edit forms for better UX
6. **Timestamps**: Auto-tracking of creation/update times for audit trail

### Potential Improvements:

- [ ] Add user authentication
- [ ] Implement Django Forms for better validation
- [ ] Add pagination for large TODO lists
- [ ] Implement filtering (by status, date)
- [ ] Add categories/tags
- [ ] Export TODOs to CSV/JSON
- [ ] Add API endpoints (Django REST Framework)
- [ ] Implement search functionality
- [ ] Add priority levels
- [ ] Email reminders for due dates

---

## 📚 Learning Outcomes

Through this project, you learned:
- How to set up a Django project from scratch
- Database modeling and migrations
- Implementing CRUD operations
- Working with templates and static files
- Writing and running tests
- URL routing and view logic
- Form handling and validation
- Using `uv` as a package manager
- Django project structure and conventions

---

## 🐛 Troubleshooting

### Common Issues:

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Migration errors:**
```bash
# Reset migrations (development only)
rm db.sqlite3
rm todos/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Import errors:**
```bash
# Ensure virtual environment is activated
source ../.venv/bin/activate
```

---

## 📞 Support

For homework-related questions, refer to:
- [HOMEWORK_ANSWERS.md](./HOMEWORK_ANSWERS.md) - Specific homework solutions
- Django Documentation: https://docs.djangoproject.com/
- AI Dev Tools Zoomcamp Materials

---

## ✅ Completion Checklist

- [x] Django installed with `uv`
- [x] Project and app created
- [x] Models defined with proper fields
- [x] Migrations created and applied
- [x] Views implemented for CRUD
- [x] URLs configured
- [x] Templates created with styling
- [x] Tests written and passing (11/11)
- [x] Application running successfully
- [x] All homework questions answered
- [x] Documentation completed

---

**Project Status:** ✅ Complete and Functional

**Last Updated:** November 23, 2025
