### Routes Module

**Purpose:**
The `routes` folder contains API route handlers that define endpoints and interact with the services layer.

**Contents:**
- `events.py` → Event booking-related routes.
- `auth.py` → Authentication and user management routes.
- `admin.py` → Admin dashboard-related endpoints.

**Example Usage:**
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}
```
