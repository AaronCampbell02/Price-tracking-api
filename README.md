# Price-tracking-api
This project is a backend  REST API service that scrapes prices from product pages built for https://www.currys.co.uk/, updates price every hour, storing the history of selected items.

The project works through creating a docker container, which runs application.py. This starts a scheduler, which scrapes the price from all stored product every set time period (1 hour). The website is scraped using cloudscraper, this was used to overcome original errors when attempting to scrape using the original HTTP client requests. The new price for each product is stored in PostgreSQL database, which is FLASK exposes through a REST API. Pytest is utilised to provide some tests to ensure the system is working correctly, as of publishing all tests pass, this is separate from live scraping issues as the tests run entirely offline through mock data.

| Method | Endpoint                  | Description                             |
|--------|---------------------------|-----------------------------------------|
| POST   | `/products`               | Add a product and scrape initial price  |
| GET    | `/products`               | List all tracked products               |
| GET    | `/products/<id>/history`  | View price history for a product        |
| DELETE | `/products/<id>`          | Remove a product and its history        |

## Tech stack:
  Python
  Flask
  PostgreSQL
  psycopg2 (connects python to Postgres)
  Beautiful soup (parses html)
  cloudscraper
  APIScheduler
  pytest
  Docker

## Architecture

Client (curl / browser)
        |
        v
   Flask App (application.py)
        |
        +--> POST /products --------> Scraper (cloudscraper + BeautifulSoup) --> PostgreSQL
        |
        +--> GET /products ----------------------------------------------------> PostgreSQL
        |
        +--> GET /products/<id>/history ------------------------------------------> PostgreSQL
        |
        +--> DELETE /products/<id> -----------------------------------------------> PostgreSQL

APScheduler (background, every 1 hour)
        |
        v
   Scraper (cloudscraper + BeautifulSoup) --> PostgreSQL


## Running the program

```
docker-compose up --build
python setupDB
Invoke-WebRequest -Uri "http://localhost:5000/products" -Method POST -ContentType "application/json" -Body '{"url": "https://www.currys.co.uk/products/apple-macbook-neo-13-2026-a18-pro-256-gb-ssd-citrus-10292844.html"}' #example page
```

## Testing the program
```
python -m pytest
```


