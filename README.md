# Webhook Transaction Processor

A robust FastAPI-based service for processing financial transactions via webhooks with database persistence and background task handling.

## 🚀 Live Deployment

**Base URL**: `https://webhook-transaction-processor.onrender.com`

The service is deployed and ready to test. No local setup required!

---

## 📮 Quick Start with Postman

### 1. Health Check
- **Method**: GET
- **URL**: `https://webhook-transaction-processor.onrender.com/`
- **Expected Response** (200 OK):
  ```json
  {
    "status": "HEALTHY",
    "current_time": "2025-12-26T10:30:45.123456"
  }
  ```

### 2. Submit a Transaction Webhook
- **Method**: POST
- **URL**: `https://webhook-transaction-processor.onrender.com/v1/webhooks/transactions`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "transaction_id": "txn_001_unique",
    "source_account": "ACC001",
    "destination_account": "ACC002",
    "amount": 1000.00,
    "currency": "USD"
  }
  ```
- **Expected Response** (202 Accepted):
  ```json
  {
    "message": "accepted"
  }
  ```
- **⚠️ Note**: Change `transaction_id` for each test to avoid duplicates. The system processes transactions asynchronously (30-second processing time).

### 3. Get Transaction Status
- **Method**: GET
- **URL**: `https://webhook-transaction-processor.onrender.com/v1/transactions/txn_001_unique`
- **Expected Response** (200 OK):
  ```json
  {
    "id": "uuid-here",
    "transaction_id": "txn_001_unique",
    "source_account": "ACC001",
    "destination_account": "ACC002",
    "amount": 1000.00,
    "currency": "USD",
    "status": "PROCESSED",
    "created_at": "2025-12-26T10:00:00",
    "processed_at": "2025-12-26T10:00:30"
  }
  ```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check - verify service is running |
| POST | `/v1/webhooks/transactions` | Submit a transaction for processing |
| GET | `/v1/transactions/{transaction_id}` | Retrieve transaction status and details |

---

## ✨ Key Features

- ✅ **Immediate Response**: Returns 202 Accepted instantly (non-blocking)
- ✅ **Async Processing**: Transactions processed in the background
- ✅ **Idempotency**: Duplicate transactions with same ID are safely ignored
- ✅ **Data Persistence**: All transactions stored in PostgreSQL
- ✅ **Interactive Docs**: Access at `/docs` (Swagger UI) or `/redoc`

---

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Deployment**: Render

---

## 📡 Testing with cURL

```bash
# Health check
curl https://webhook-transaction-processor.onrender.com/

# Submit transaction
curl -X POST https://webhook-transaction-processor.onrender.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_001",
    "source_account": "ACC001",
    "destination_account": "ACC002",
    "amount": 500.00,
    "currency": "USD"
  }'

# Get transaction status
curl https://webhook-transaction-processor.onrender.com/v1/transactions/txn_test_001
```

---

## 📖 Interactive API Documentation

Try the endpoints directly in your browser:
- **Swagger UI**: https://webhook-transaction-processor.onrender.com/docs
- **ReDoc**: https://webhook-transaction-processor.onrender.com/redoc

---

## 🏗 Architecture

**Webhook Pattern**: Accepts requests immediately (202 Accepted) and processes asynchronously

- **API Layer**: FastAPI validates and accepts transaction payloads
- **Database Layer**: SQLAlchemy ORM persists to PostgreSQL
- **Service Layer**: Background tasks process transactions asynchronously
- **Benefits**: Non-blocking, scalable, reliable, idempotent

---

## 📊 Transaction Lifecycle

1. **Webhook Received** → Transaction created with status `PROCESSING`
2. **202 Accepted** → Response sent immediately
3. **Background Processing** → Processed asynchronously (30 sec)
4. **Status Updated** → Transaction marked as `PROCESSED`
5. **Query Status** → Use GET endpoint to check latest state

---

## 🔧 Local Development (Optional)

### Prerequisites
- Python 3.8+, PostgreSQL, pip

### Setup
```bash
git clone <repository-url>
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Configure database
echo "DATABASE_URL=postgresql://user:password@host:port/database" > .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for local testing.

---

## 📧 Support

For issues or questions, please reach out to the development team.
