### Infrastructure Module

**Purpose:**
The `infrastructure` folder manages connections to external services such as databases, AWS, and third-party APIs.

**Contents:**
- `database.py` → Database connection setup (MongoDB/PostgreSQL/Redshift).
- `aws_clients.py` → AWS CloudWatch and Redshift clients.
- `email_service.py` → Email sending and notification handling.

**Example Usage:**
```python
from infrastructure.database import Database

db = Database()
connection = db.get_connection()
