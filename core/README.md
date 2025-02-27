### Core Module

**Purpose:**
The `core` folder contains essential utilities, exception handling, and shared logic used throughout the project.

**Contents:**
- `exceptions.py` → Custom exception classes for error handling.
- `utils.py` → Common utility functions (e.g., date formatting, logging, etc.).
- `config.py` → Loads environment variables and settings.

**Example Usage:**
```python
from core.exceptions import CustomError

try:
    raise CustomError("Something went wrong!")
except CustomError as e:
    print(e)
```
