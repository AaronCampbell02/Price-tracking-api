import pytest
from scraper import parse_price, parse_name


def test_parse_price_valid():
    fake = '<span class="value" content="699.00">£699.00</span>'
    assert parse_price(fake) == "699.00"


def test_parse_price_missing_element():
    html = "<html><body>No price here</body></html>"
    with pytest.raises(ValueError):
        parse_price(html)


def test_parse_name_valid():
    fake = '<h1 class="product-name">Apple MacBook Neo 13 2026</h1>'
    assert parse_name(fake) == "Apple MacBook Neo 13 2026"


def test_parse_name_missing_element():
    html = "<html><body>No title here</body></html>"
    with pytest.raises(ValueError):
        parse_name(html)