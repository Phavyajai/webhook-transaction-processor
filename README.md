# Webhook Transaction Processor

A robust FastAPI-based service for processing financial transactions via webhooks with database persistence and background task handling.

## Overview

This project provides a webhook-based transaction processing system that accepts transaction payloads, stores them in a PostgreSQL database, and processes them asynchronously. It's built with FastAPI for high performance and uses SQLAlchemy as the ORM with Alembic for database migrations.

## Features

- **Webhook Endpoint**: RESTful API to receive transaction data
- **Async Processing**: Background task processing for non-blocking operations
- **Database Persistence**: PostgreSQL integration with SQLAlchemy ORM
- **Idempotency**: Handles duplicate webhook payloads gracefully
- **Health Checks**: Built-in status endpoint
- **Database Migrations**: Alembic for version control of database schema
- **Environment Configuration**: Secure configuration management with `.env`

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Python Version**: 3.8+

## Project Structure

```
webhook-transaction-processor/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment configuration
│   └── script.py.mako          # Migration script template
├── app/
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── db/
│   │   ├── models.py           # SQLAlchemy models
│   │   └── session.py          # Database session management
│   ├── schemas/
│   │   └── transaction.py       # Pydantic schemas (request/response)
│   ├── services/
│   │   └── processor.py         # Business logic for transaction processing
│   └── main.py                 # FastAPI application setup
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic configuration
└── .env                        # Environment variables (not versioned)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip or poetry for dependency management

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Running the Service

### Development Mode

Start the server with auto-reload for development:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `--reload`: Auto-restarts the server when code changes
- `--host 0.0.0.0`: Listen on all network interfaces
- `--port 8000`: Run on port 8000

### Production Mode

Start with Gunicorn for production:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Verify the Service

Check if the service is running:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "HEALTHY",
  "current_time": "2025-12-26T10:30:45.123456"
}
```

## Testing

### Manual Testing with cURL

**Test webhook endpoint:**
```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_001",
    "source_account": "ACC001",
    "destination_account": "ACC002",
    "amount": 1000.00,
    "currency": "USD"
  }'
```

Expected response (202 Accepted):
```json
{"message": "accepted"}
```

**Retrieve transaction status:**
```bash
curl http://localhost:8000/v1/transactions/txn_test_001
```

### Automated Testing

Create a `test_api.py` file:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_webhook_accept():
    payload = {
        "transaction_id": "txn_test_123",
        "source_account": "ACC001",
        "destination_account": "ACC002",
        "amount": 1000.00,
        "currency": "USD"
    }
    response = client.post("/v1/webhooks/transactions", json=payload)
    assert response.status_code == 202
    assert response.json()["message"] == "accepted"

def test_duplicate_webhook():
    payload = {
        "transaction_id": "txn_duplicate_123",
        "source_account": "ACC001",
        "destination_account": "ACC002",
        "amount": 500.00,
        "currency": "USD"
    }
    response1 = client.post("/v1/webhooks/transactions", json=payload)
    response2 = client.post("/v1/webhooks/transactions", json=payload)
    assert response1.status_code == 202
    assert response2.status_code == 202  # Idempotent
```

Run tests:
```bash
pip install pytest
pytest
```

## API Endpoints

### Health Check
- **GET** `/`
  - Returns server status and current timestamp
  - Response: `{"status": "HEALTHY", "current_time": "2025-12-26T..."}`

### Receive Transaction Webhook
- **POST** `/v1/webhooks/transactions`
  - Accepts transaction payload and queues for processing
  - Status Code: `202 Accepted`
  - Request Body:
    ```json
    {
      "transaction_id": "txn_123456",
      "source_account": "ACC001",
      "destination_account": "ACC002",
      "amount": 1000.00,
      "currency": "USD"
    }
    ```
  - Response: `{"message": "accepted"}`

### Get Transaction Details
- **GET** `/v1/transactions/{transaction_id}`
  - Retrieves transaction status and details
  - Response: Transaction object with status, timestamps, and metadata

## Database Schema

### Transactions Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| transaction_id | String | Unique transaction identifier |
| source_account | String | Source account number |
| destination_account | String | Destination account number |
| amount | Numeric(12,2) | Transaction amount |
| currency | String | Currency code (e.g., USD, EUR) |
| status | String | Current status (PROCESSING, COMPLETED, FAILED) |
| created_at | DateTime | Creation timestamp |
| processed_at | DateTime | Processing completion timestamp |

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

### Code Style

Format code with:
```bash
black app/
```

Lint with:
```bash
flake8 app/
```

## Configuration

Environment variables in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |

## Error Handling

- **Duplicate Webhooks**: The system automatically handles idempotency by catching `IntegrityError` on duplicate `transaction_id` and returning `202 Accepted`
- **Database Errors**: Transactions are rolled back on failure
- **Background Tasks**: Failed background tasks log errors but don't affect the initial webhook response

## Performance Considerations

- Background task processing ensures webhook responses are immediate
- Connection pooling through SQLAlchemy optimizes database access
- Uvicorn's async workers handle concurrent requests efficiently

## Technical Choices

### Why FastAPI?

- **High Performance**: Built on Starlette and Pydantic, offering some of the fastest Python frameworks
- **Async/Await Support**: Native async/await enables non-blocking I/O for handling concurrent webhook requests
- **Automatic API Documentation**: Generates interactive Swagger UI and ReDoc documentation automatically
- **Data Validation**: Pydantic schemas provide automatic request/response validation with minimal code
- **Type Hints**: Full type hint support improves code quality and IDE support

### Why PostgreSQL?

- **Reliability**: ACID compliance ensures transaction data integrity
- **Scalability**: Handles high transaction volumes with connection pooling
- **Advanced Features**: Native JSON, UUID, and Numeric types suit financial data well
- **Industry Standard**: Widely used in production for financial applications

### Why SQLAlchemy ORM?

- **Database Agnostic**: Easily switch databases if needed
- **Relationship Mapping**: Simplifies managing complex data relationships
- **Query Building**: Object-oriented query interface is safer than raw SQL
- **Lazy Loading & Eager Loading**: Optimizes database queries

### Why Alembic for Migrations?

- **Version Control for Schema**: Track all database changes in version control
- **Reversible**: Easy rollback to previous schema versions
- **Autogenerate**: Automatically detects model changes
- **SQLAlchemy Integration**: Seamless integration with SQLAlchemy

### Background Tasks Approach

- **Non-Blocking Webhooks**: Immediately returns 202 Accepted to the client
- **Asynchronous Processing**: Long-running operations don't block webhook endpoint
- **Idempotency**: Duplicate webhooks with same transaction_id are safely handled
- **Reliability**: If a task fails, the webhook is already accepted and can be retried

### Why This Architecture?

1. **Webhook Pattern**: Fits the asynchronous nature of transaction processing systems
2. **Separation of Concerns**: API layer, database layer, and business logic are decoupled
3. **Scalability**: Background tasks can be moved to a task queue (Celery/RQ) later
4. **Testability**: Clear interfaces make unit and integration testing straightforward

## Security

- Store sensitive credentials in `.env` (never commit)
- Use environment variables for database connection strings
- Implement authentication/authorization as needed per your requirements
- Validate all incoming webhook payloads
- Use HTTPS in production for webhook endpoints
- Implement rate limiting to prevent abuse

## Contributing

1. Create a feature branch: `git checkout -b feature/name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/name`
4. Submit a pull request

## License

Specify your project license here.

## Support

For issues and questions, please contact the development team or open an issue in the repository.
