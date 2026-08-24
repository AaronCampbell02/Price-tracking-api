import pytest
from unittest.mock import patch, MagicMock
from application import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

@patch("application.get_product_info", return_value={"name": "MacBook Neo", "price": "699.00"})
@patch("application.get_db_connection")
def test_add_product(mock_db,mock_info, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.post("/products", json={"url": "http://example.com"})
    assert response.status_code == 200
    assert response.json["name"] == "MacBook Neo"
    assert response.json["price"] == "699.00"

@patch("application.get_db_connection")
def test_get_products(mock_db, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "http://example.com", "Laptop")]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/products")
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "url": "http://example.com", "name": "Laptop"}]

@patch("application.get_db_connection")
def test_get_history(mock_db, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, 1, 699.00, "2026-08-24T12:00:00")]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/products/1/history")
    assert response.status_code == 200
    assert response.json[0]["price"] == 699.00

@patch("application.get_db_connection")
def test_delete_product(mock_db, client):
    mock_db.return_value.cursor.return_value = MagicMock()

    response = client.delete("/products/1")
    assert response.status_code == 200
    assert "deleted" in response.json["message"]