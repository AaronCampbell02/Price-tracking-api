from bs4 import BeautifulSoup
import cloudscraper


def parse_price(html):
    soup = BeautifulSoup(html, "html.parser")
    price_element = soup.find("span", class_="value")
    if not price_element or not price_element.get("content"):
        raise ValueError("Price element not found")
    return price_element["content"]


def parse_name(html):
    soup = BeautifulSoup(html, "html.parser")
    name_element = soup.find("h1", class_="product-name")
    if not name_element:
        raise ValueError("Product name element not found")
    return name_element.get_text(strip=True)


def get_product_info(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    html = response.text
    return {
        "name": parse_name(html),
        "price": parse_price(html)
    }


if __name__ == "__main__":
    url = "https://www.currys.co.uk/products/apple-macbook-neo-13-2026-a18-pro-256-gb-ssd-citrus-10292844.html"
    print(get_product_info(url))