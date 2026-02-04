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

**Note:** Ensure Docker Desktop is running before proceeding.

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

**Sample Request:** 
```http
POST http://localhost:8000/orders/
```

**Sample Payload:**
```json
{
  "store_id": 1,
  "items": [
    {"product_id": 1, "quantity": 2}

  ]
}
```

**Sample Response:**
```json
{
  "id": 4,
  "status": "CONFIRMED",
  "created_at": "2026-02-04T18:02:35.899432+05:45",
  "items": [
    {
      "product": 1,
      "quantity_requested": 2
    }
  ]
}
```
**Description:**
- CONFIRMED - stock available, quantities deducted

- REJECTED - insufficient stock, no deduction


###  2. Product Search API

**Endpoint:** 
```http
GET http://localhost:8000/api/search/products/
```


**Sample Request:** 
```http
GET http://localhost:8000/api/search/products/?q=iphone&store_id=2&in_stock=true&sort=price
```

| Parameter | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| q | string | No | Keyword search (title, description, category) |
| category | string | No | Filter by category name |
| min_price | number | No | Minimum price |
| max_price | number | No | Maximum price |
| store_id | integer | No | Filter products available in a store |
| in_stock | boolean | No | Only return in-stock products |
| sort | string | No | price, newest, relevance |
| page | integer | No | Pagination page number |


**Sample Response:**
```json
{
  "count": 120,
  "next": "/api/search/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 5,
      "title": "Smartphone X",
      "price": 799,
      "category": "Electronics"
    }
  ]
}

```


**Description:** Search products with keyword, category, price range, sorting, and pagination.

### 3. Store Order Listing

**Endpoint:** 
```http
GET http://localhost:8000/stores/{store_id}/orders/
```


**Sample Request:** 
```http
GET http://localhost:8000/stores/1/orders/
```

**Sample Response:**
```json
[
    {
        "id": 4,
        "status": "CONFIRMED",
        "created_at": "2026-02-04T18:02:35.899432+05:45",
        "total_items": 1
    },
    {
        "id": 3,
        "status": "REJECTED",
        "created_at": "2026-02-04T18:02:08.262993+05:45",
        "total_items": 0
    }
]
```

**Description:** Return a list of all orders belonging to the store:

### 4. Inventory Listing

**Endpoint:** 
```http
GET http://localhost:8000/stores/{store_id}/inventory/
```


**Sample Request:** 
```http
GET http://localhost:8000/stores/1/inventory/
```

**Sample Response:**
```json
[
  {
    "product_title": "Advanced Adapter 186",
    "price": "743.27",
    "category": "Toys",
    "quantity": 83
  },
  {
    "product_title": "Advanced Adapter 360",
    "price": "373.74",
    "category": "Home & Garden",
    "quantity": 95
  },
]

```

**Description:** Return inventory items for that store.

### 5. Autocomplete

**Endpoint:** 
```http
GET http://localhost:8000/api/search/suggest/
```

**Query Parameters:**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| q | string | Yes | Search prefix (minimum 3 characters) |

**Sample Request:** 
```http
GET http://localhost:8000/api/search/suggest/?q=mon
```

**Sample Response:**
```json
[
  "Standard Monitor 2",
  "Professional Monitor 70",
  "Advanced Monitor 82",
  "Ultra Monitor 94",
  "Ultra Monitor 115",
  "Super Monitor 116",
  "Compact Monitor 128",
  "Basic Monitor 145",
  "Professional Monitor 153",
  "Super Monitor 161"
]

```


**Description:** Returns up to 10 product titles starting with the query prefix (iph). Minimum 3 characters required.



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







