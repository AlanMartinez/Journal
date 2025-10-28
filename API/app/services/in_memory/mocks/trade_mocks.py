from datetime import date, datetime

TRADE_MOCK_DATA = {
    "1": {
        "id": "1",
        "symbol": "NQ",
        "side": "buy",
        "rate": 2.5,
        "entry": 35000.50,
        "stop_loss": 34500.00,
        "take_profit": 36000.00,
        "status": "TP",
        "result": 95.50,
        "date": "2025-10-28",
        "notes": "Trade de prueba exitoso",
        "link": "https://www.binance.com/es/trade/BTC_USDT"
    },
    "2": {
        "id": "2",
        "symbol": "NQ",
        "side": "sell",
        "rate": 2,
        "entry": 1850.75,
        "stop_loss": 1900.00,
        "take_profit": 1800.00,
        "status": "SL",
        "result": -49.25,
        "date": "2025-10-27",
        "notes": "Stop loss alcanzado",
        "link": "https://www.binance.com/es/trade/ETH_USDT"
    }
}
