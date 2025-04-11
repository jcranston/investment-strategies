from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_simulate_daily():
    response = client.post(
        "/simulate",
        json={
            "strategy": "daily",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "tickers": ["AAPL", "MSFT"],
            "initial_value": 1000000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "portfolio" in data
    assert len(data["portfolio"]) > 0
    assert isinstance(data["portfolio"][0]["Portfolio"], (int, float))


def test_simulate_rolling():
    response = client.post(
        "/simulate",
        json={
            "strategy": "rolling",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "tickers": ["AAPL", "MSFT"],
            "initial_value": 1000000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "portfolio" in data
    assert len(data["portfolio"]) > 0
    assert isinstance(data["portfolio"][0]["Portfolio"], (int, float))
