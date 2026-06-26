# Myntra Product Scraper API

## Overview

This project is a FastAPI-based backend tool that imports Myntra product IDs from a CSV file, scrapes product information from publicly accessible Myntra product pages, stores the data in a SQLite database, and exposes APIs to retrieve product details.

The application follows a simple layered architecture using Routers, Services, Repositories, and SQLAlchemy models.



## Features

* Import product IDs from a CSV file.
* Fetch product details from public Myntra pages.
* Store products and categories in SQLite.
* Store the first three sponsored products for each category.
* Return product details from the database whenever available.
* Automatically scrape and store products that are not already present in the database.
* JSON API responses.
* Handles missing data and scraping failures gracefully.



## Tech Stack

* Python 3.8+
* FastAPI
* SQLAlchemy
* SQLite
* BeautifulSoup4
* Requests
* Uvicorn


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
git clone <repository-url>
cd <repository-folder>


### Create Virtual Environment
python -m venv venv

### Activate Virtual Environment
source venv/bin/activate

### Install Dependencies
pip install -r requirements.txt


### Run the Application
uvicorn app.main:app --reload


Open Swagger UI:
http://127.0.0.1:8000/docs


---

## Approach

The application is divided into separate layers.

-Router: handles HTTP requests.
-Service: contains business logic.
-Repository : performs database operations.
-Models : define database tables.
-Myntra Service :handles web scraping.


## Assumptions

-Product IDs provided in the CSV are valid Myntra product IDs.
-Product information is available on public product pages.

## Error Handling

The application handles:

-Invalid CSV files
-uplicate product IDs
-Duplicate categories
-Missing product data
-HTTP request failures


## Future Improvements

With additional time, the following improvements could be added:
- Authentication:
- Myntra public API
- Background jobs
- FrontEnd UI


