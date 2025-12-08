Setup and `uv` usage

This backend folder contains an OpenAPI specification derived from the frontend's `MockAPI` client.

Recommended steps to initialize a Python backend using `uv` (dependency and env manager):

1. Install `uv` (if not installed):

```bash
pip install uv
```

2. Initialize the backend project (creates lockfile and minimal config):

```bash
cd backend
uv init
```

3. Sync dependencies from lockfile (after `uv init` or when lockfile changes):

```bash
uv sync
```

4. Add packages as needed while developing (example: FastAPI + Uvicorn):

```bash
uv add fastapi uvicorn pydantic
```

5. Run Python files using `uv` so they use the environment managed by `uv`:

```bash
uv run python main.py
```

Notes:
- The `openapi.yaml` in this folder describes the endpoints the frontend expects. Implement the backend routes to match these paths, request bodies and responses.
- When you want, I can scaffold a minimal FastAPI app that implements these endpoints (mocked behavior matching the current `MockAPI`) so the frontend can talk to a real HTTP backend.
