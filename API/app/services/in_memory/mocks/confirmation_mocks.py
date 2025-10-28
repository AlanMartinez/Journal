from datetime import datetime, timezone

CONFIRMATION_MOCK_DATA = {
    "1": {
        "id": "1",
        "trade_id": "1",
        "confirmation_type": "entry",
        "price": 35000.50,
        "timestamp": datetime(2025, 10, 28, 10, 30, 0, tzinfo=timezone.utc).isoformat(),
        "notes": "Entrada confirmada"
    },
    "2": {
        "id": "2",
        "trade_id": "1",
        "confirmation_type": "exit",
        "price": 36000.00,
        "timestamp": datetime(2025, 10, 28, 15, 45, 0, tzinfo=timezone.utc).isoformat(),
        "notes": "Take profit alcanzado"
    }
}
