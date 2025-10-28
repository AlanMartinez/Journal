from datetime import datetime, timezone

EMOTION_MOCK_DATA = {
    "1": {
        "id": "1",
        "trade_id": "1",
        "emotion_type": "before",
        "confidence": 0.8,
        "emotion": "confident",
        "notes": "Sintiéndome seguro con este trade",
        "timestamp": datetime(2025, 10, 28, 10, 20, 0, tzinfo=timezone.utc).isoformat()
    },
    "2": {
        "id": "2",
        "trade_id": "1",
        "emotion_type": "after",
        "confidence": 0.9,
        "emotion": "satisfied",
        "notes": "Buen trade, seguí mi plan",
        "timestamp": datetime(2025, 10, 28, 15, 50, 0, tzinfo=timezone.utc).isoformat()
    }
}
