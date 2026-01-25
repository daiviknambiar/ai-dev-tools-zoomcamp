# Testing Guide

This document describes the testing strategy, how to run tests, and guidelines for writing new tests.

---

## Table of Contents

- [Testing Strategy](#testing-strategy)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Continuous Integration](#continuous-integration)

---

## Testing Strategy

The project uses a multi-layered testing approach:

```
┌─────────────────────────────────┐
│     Integration Tests (E2E)     │  ← Full system workflows
├─────────────────────────────────┤
│     Integration Tests (API)     │  ← API endpoint testing
├─────────────────────────────────┤
│        Unit Tests              │  ← Individual components
└─────────────────────────────────┘
```

### Test Types

1. **Unit Tests**: Test individual functions and classes in isolation
2. **Integration Tests**: Test API endpoints with mocked external dependencies
3. **Component Tests**: Test frontend components (limited due to Streamlit nature)

### Coverage Goals

- **Minimum**: 70% code coverage
- **Target**: 80%+ code coverage
- **Critical paths**: 100% coverage

---

## Test Structure

### Backend Tests

```
backend/tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── test_nba_api_client.py      # API client unit tests
└── integration/
    ├── __init__.py
    └── test_endpoints.py             # Endpoint integration tests
```

### Frontend Tests

```
frontend/tests/
├── __init__.py
├── test_api_client.py                # API client tests
└── test_components.py                # Component tests
```

---

## Running Tests

### Prerequisites

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-cov pytest-asyncio pytest-mock
```

### Backend Tests

#### Run All Tests

```bash
cd backend
pytest
```

#### Run with Coverage

```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term-missing
```

#### Run Specific Test Types

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_nba_api_client.py -v

# Specific test function
pytest tests/unit/test_nba_api_client.py::TestNBAAPIClient::test_get_players_success -v
```

#### Watch Mode (Auto-rerun on Changes)

```bash
pip install pytest-watch
cd backend
ptw -- --cov=app
```

### Frontend Tests

```bash
cd frontend
pytest -v
```

### Docker Tests

Run tests inside Docker containers:

```bash
# Backend tests
docker-compose run backend pytest --cov=app

# Frontend tests
docker-compose run frontend pytest
```

---

## Test Coverage

### View Coverage Report

After running tests with coverage:

```bash
# Terminal output
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Coverage Report Example

```
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
app/__init__.py                             0      0   100%
app/main.py                                35      2    94%   45-46
app/config.py                              15      0   100%
app/services/nba_api_client.py            120      8    93%   156-160, 245
app/api/routes/players.py                  45      3    93%   78-80
app/api/routes/games.py                    38      4    89%   92-95
app/api/routes/health.py                    8      0   100%
---------------------------------------------------------------------
TOTAL                                     261     17    93%
```

---

## Writing Tests

### Backend Unit Test Example

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.nba_api_client import NBAAPIClient

@pytest.fixture
def nba_client():
    """Create NBA API client for testing."""
    return NBAAPIClient()

@pytest.fixture
def mock_httpx_client():
    """Create mock httpx client."""
    return AsyncMock()

@pytest.mark.asyncio
async def test_get_player_success(nba_client, mock_httpx_client):
    """Test successful player retrieval."""
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {"id": 237, "first_name": "LeBron"}
    }
    mock_response.raise_for_status = MagicMock()
    mock_httpx_client.request = AsyncMock(return_value=mock_response)
    nba_client._client = mock_httpx_client
    
    # Act
    result = await nba_client.get_player(237)
    
    # Assert
    assert result["id"] == 237
    assert result["first_name"] == "LeBron"
```

### Backend Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.nba_api_client import get_nba_client

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

@pytest.fixture
def mock_nba_client():
    """Create mock NBA API client."""
    return AsyncMock()

def test_list_players_success(client, mock_nba_client):
    """Test listing players successfully."""
    # Arrange
    mock_nba_client.get_players.return_value = {
        "data": [{"id": 237, "first_name": "LeBron"}],
        "meta": {"current_page": 1}
    }
    app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
    
    # Act
    response = client.get("/api/v1/players?search=LeBron")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    
    # Cleanup
    app.dependency_overrides.clear()
```

### Frontend Test Example

```python
import pytest
import requests_mock
from services.api_client import APIClient

def test_get_players_success():
    """Test successful player list retrieval."""
    # Arrange
    api_client = APIClient(base_url="http://test:8000")
    
    with requests_mock.Mocker() as m:
        m.get(
            "http://test:8000/api/v1/players",
            json={"data": [{"id": 237, "first_name": "LeBron"}]}
        )
        
        # Act
        result = api_client.get_players(search="LeBron")
        
        # Assert
        assert "data" in result
        assert len(result["data"]) == 1
```

### Testing Best Practices

1. **Arrange-Act-Assert Pattern**: Structure tests clearly
2. **One Assertion Per Test**: Focus on single behavior
3. **Descriptive Names**: `test_get_player_returns_404_when_not_found`
4. **Use Fixtures**: Reuse common setup code
5. **Mock External Dependencies**: Don't call real APIs in tests
6. **Test Edge Cases**: Empty lists, null values, errors
7. **Test Error Handling**: Verify exceptions are raised correctly

---

## Testing Checklist

### Before Committing

- [ ] All tests pass locally
- [ ] New code has tests
- [ ] Coverage hasn't decreased
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases are covered
- [ ] Error scenarios are tested

### Test Categories to Cover

- [ ] **Happy Path**: Normal, expected usage
- [ ] **Edge Cases**: Empty inputs, boundary values
- [ ] **Error Cases**: Invalid inputs, API failures
- [ ] **Integration**: Components work together
- [ ] **Performance**: No obvious slowdowns

---

## Continuous Integration

Tests run automatically on every push via GitHub Actions:

### CI Workflow

```yaml
- Run linting (flake8, black)
- Run unit tests
- Run integration tests
- Build Docker images
- Run tests in Docker
- Generate coverage report
```

### Viewing CI Results

1. Go to GitHub repository
2. Click "Actions" tab
3. Select workflow run
4. View test results and logs

### Local CI Simulation

Run the same checks as CI locally:

```bash
# Lint
cd backend
flake8 app --count --select=E9,F63,F7,F82 --show-source
black --check app

# Test
pytest --cov=app --cov-report=term-missing

# Build Docker
docker-compose build
docker-compose up -d
docker-compose down
```

---

## Debugging Failed Tests

### View Detailed Output

```bash
pytest -vv  # Very verbose
pytest -s   # Show print statements
pytest --pdb  # Drop into debugger on failure
```

### Debug Specific Test

```bash
pytest tests/unit/test_nba_api_client.py::test_get_player_success -vv -s
```

### Common Test Failures

#### 1. Import Errors

**Cause**: Missing dependencies or incorrect PYTHONPATH

**Solution**:
```bash
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. Async Test Failures

**Cause**: Missing pytest-asyncio or incorrect markers

**Solution**:
```bash
pip install pytest-asyncio
# Add to test: @pytest.mark.asyncio
```

#### 3. Mock Not Working

**Cause**: Mocking wrong import path

**Solution**:
```python
# Mock where it's used, not where it's defined
# Wrong: @patch('app.services.nba_api_client.httpx')
# Right: @patch('app.api.routes.players.get_nba_client')
```

---

## Performance Testing

### Load Testing Backend

```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

### Example Locustfile

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_players(self):
        self.client.get("/api/v1/players?search=LeBron")
    
    @task
    def get_live_games(self):
        self.client.get("/api/v1/games/live")
```

---

## Next Steps

- Set up test coverage reporting to Codecov
- Add performance benchmarks
- Implement visual regression testing for frontend
- Add end-to-end tests with Playwright/Selenium
- Set up mutation testing with `mutmut`

---

**Questions?** Open an issue or check the CI logs for examples.
