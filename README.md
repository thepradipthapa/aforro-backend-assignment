# Aforro Backend Assignment


## 🔧 Setup Instructions


### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- UV package manager (optional for local development)

### Local Development

#### 1. Clone the repository

```bash
git clone https://github.com/thepradipthapa/aforro-backend-assignment.git

cd aforro-backend-assignment
```

### 2. Install UV (if not already installed)

```bash 
pip install uv
```

Note: Ensure Docker Desktop is running before proceeding.

### 3. Create Environment File
- Create a .env file in the project root:
- Edit .env with your configuration:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-q_c7hyaz0!qeq&@33z7lfc^qw19^3hz_7yj45+@b11n*cyitmg

# Database configuration
POSTGRES_DB=dev_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432


# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL = redis://redis:6379/0
```


### 4. build and start container
```bash
# Build Docker images
docker-compose build

# Start all services (Django, PostgreSQL, Redis, Celery)
docker-compose up
```


### 5. Run Test
```bash
# Run all the test case
docker exec -it aforro_app uv run pytest
```

### 6. Seed dummy data
```bash
# Generate dummy Data for development
docker exec -it aforro_app uv run python manage.py seed_data
```

---

## 📌 Sample API Requests


### 1. Create Order

**Endpoint:** `POST http://localhost:8000/orders/`

**Payload:**
```json
{
  "store_id": 1,
  "items": [
    {"product_id": 5, "quantity_requested": 2},
    {"product_id": 10, "quantity_requested": 1}
  ]
}
```
**Response:**

CONFIRMED → stock available, quantities deducted

REJECTED → insufficient stock, no deduction


###  2. Product Search API

**Endpoint:** `GET http://localhost:8000/api/search/products/?q=iphone&store_id=2&in_stock=true&sort=price`

**Description:** Search products with keyword, category, price range, sorting, and pagination.

### 3. Store Order Listing

**Endpoint:** `GET http://localhost:8000/stores/1/orders/`

**Description:** Return a list of all orders belonging to the store:

### 4. Inventory Listing
**Endpoint:** `GET http://localhost:8000/stores/1/inventory/`

**Description:** Return inventory items for that store including:

### 5. Autocomplete
**Endpoint:** `GET http://localhost:8000/api/search/suggest/?q=iph`

**Description:** eturns up to 10 product titles starting with the query prefix (iph). Minimum 3 characters required.



---

## Notes on Caching & Async Logic

### Redis Caching
- Product search results are cached based on query parameters, filters, and sorting.
- TTL ensures cache freshness.
- Reduces repeated database queries for frequent searches.
- Guarantees fast API responses.

### Celery Asynchronous Tasks
- Used for order processing:
  1. Order created via API
  2. Task dispatched with `send_order_confirmation.delay(order_id)`
  3. Worker consumes task, checks inventory, and updates order status
- Non-blocking API responses.
- Can scale by adding more Celery workers.


## Scalability Considerations

- **Stateless API:** Django views are stateless- can scale horizontally with load balancer.
- **Redis caching:** Reduces database read pressure for frequently requested data (product search, autocomplete).
- **Celery workers:** Background tasks can scale independently; adding more workers handles more async load.
- **PostgreSQL transactions:** Ensure order consistency under high concurrency.
- **Dockerized services:** Easy deployment
- **Future improvements:** 
  - Rate limiting using Redis
  - Full-text search or Elasticsearch for faster product search
  - Read replicas for PostgreSQL
  - Monitoring Celery tasks







