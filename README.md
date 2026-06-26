# Myntra Product Scraper API

## Overview

This project is a FastAPI-based backend tool that imports Myntra product IDs from a CSV file, scrapes product information from publicly accessible Myntra product pages, stores the data in a SQLite database, and exposes APIs to retrieve product details.

The application follows a simple layered architecture using Routers, Services, Repositories, and SQLAlchemy models.

---

## Features

* Import product IDs from a CSV file.
* Fetch product details from public Myntra pages.
* Store products and categories in SQLite.
* Prevent duplicate products and categories.
* Store the first three sponsored products for each category.
* Return product details from the database whenever available.
* Automatically scrape and store products that are not already present in the database.
* JSON API responses.
* Handles missing data and scraping failures gracefully.

---

## Tech Stack

* Python 3.8+
* FastAPI
* SQLAlchemy
* SQLite
* BeautifulSoup4
* Requests
* Uvicorn

---

## Project Structure

```
app
├── api
├── config
├── db
├── models
├── repositories
├── schemas
├── services
└── main.py

requirements.txt
README.md
```

---

## Database Design

### Category

| Column             |
| ------------------ |
| id                 |
| name               |
| sponsored_products |

### Product

| Column       |
| ------------ |
| id           |
| product_id   |
| title        |
| description  |
| image_urls   |
| rating       |
| rating_count |
| brand        |
| price        |
| currency     |
| category_id  |

---

## API Endpoints

### Import Products

```
POST /products/import
```

Upload a CSV file containing a `product_id` column.

Example:

| product_id |
| ---------- |
| 35512522   |
| 12345678   |

Response

```json
{
  "total_products": 10,
  "imported_products": 9,
  "failed_products": 1,
  "errors": [
    "12345678 : Product not found"
  ]
}
```

---

### Get Product

```
GET /products/{product_id}
```

Workflow:

* Check if the product exists in the database.
* If found, return the stored data.
* If not found:

  * Scrape the product page.
  * Create the category if it does not exist.
  * Store the product.
  * Return the product details.

---

## How to Run

### Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Approach

The application is divided into separate layers.

* **Router** handles HTTP requests.
* **Service** contains business logic.
* **Repository** performs database operations.
* **Models** define database tables.
* **Myntra Service** handles web scraping.

This separation keeps the code organized and easier to maintain.

---

## Assumptions

* Product IDs provided in the CSV are valid Myntra product IDs.
* Product information is available on public product pages.
* Sponsored products are stored when a category is first created and reused for subsequent requests.
* SQLite is sufficient for this assignment.

---

## Error Handling

The application handles:

* Invalid CSV files
* Duplicate product IDs
* Duplicate categories
* Missing product data
* HTTP request failures
* Parsing failures
* Network timeouts

Errors are collected and returned in the import response without stopping the entire import process.

---

## Scope

### Included

* CSV import
* Product scraping
* SQLite storage
* Duplicate prevention
* Sponsored product extraction
* JSON API responses
* Layered project structure

### Not Included

* Authentication
* Docker
* Deployment
* Background jobs
* Scheduled data refresh
* Frontend UI

---

## Future Improvements

With additional time, the following improvements could be added:

* Refresh sponsored products periodically.
* Retry mechanism for failed requests.
* Better logging.
* Unit and integration tests.
* PostgreSQL support.
* Frontend dashboard for uploading CSV files and viewing results.

---
