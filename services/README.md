### Service Module

**Purpose:**
The `service` folder contains business logic and core functionalities independent of API routes.

**Contents:**
- `cost_service.py` → Handles cost-related operations.
- `query_service.py` → Manages Query.
- `database_service.py` → for databases operations.

**Example Usage:**
```python
from service.event_service import EventService

query_service = QueryService()
queries = query_service.get_all_events()
```
