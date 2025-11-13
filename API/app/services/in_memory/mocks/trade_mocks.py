from datetime import date, datetime, timedelta
import random

# Generar 50 trades con variaciones en todos los campos
def generate_trade_mocks():
    """Genera 50 trades mock con variaciones en todos los campos"""
    symbols = ['NQ', 'ES', 'YM', 'CL', 'GC', 'BTC', 'ETH', 'SPY', 'QQQ', 'AAPL']
    sides = ['buy', 'sell']
    statuses = ['TP', 'SL', 'BE']
    emotions_list = ['confianza', 'miedo', 'ansiedad', 'euforia', 'duda', 'tranquilidad', 'impaciencia']
    confirmations_list = ['support', 'resistance', 'breakout', 'reversal', 'trend', 'volume']
    
    # Links de ejemplo
    trading_links = [
        "https://www.binance.com/es/trade/BTC_USDT",
        "https://www.binance.com/es/trade/ETH_USDT",
        "https://www.tradingview.com/chart/",
        "https://www.investing.com/quotes/",
        None  # Algunos sin link
    ]
    
    # Notas variadas
    notes_samples = [
        "Trade exitoso siguiendo el plan",
        "Stop loss alcanzado por volatilidad",
        "Take profit temprano por noticias",
        "Break even después de reversión",
        "Trade siguiendo señal de indicador",
        "Overtrading - tomar más cuidado",
        "Excelente ejecución del plan",
        "Sesión de trading disciplinada",
        "Trade de prueba con nueva estrategia",
        "Resultado esperado según análisis",
        None  # Algunos sin notas
    ]
    
    trades = {}
    base_date = date(2025, 10, 1)
    
    for i in range(1, 51):
        # Fecha variada (últimos 60 días)
        days_offset = random.randint(0, 60)
        trade_date = base_date - timedelta(days=days_offset)
        
        # Símbolo aleatorio
        symbol = random.choice(symbols)
        
        # Side aleatorio
        side = random.choice(sides)
        
        # Rate variado (0.5 a 5.0)
        rate = round(random.uniform(0.5, 5.0), 2)
        
        # Risk variado (algunos con risk, algunos sin)
        risk = round(random.uniform(50, 500), 2) if random.random() > 0.3 else None
        
        # Status y result relacionados
        status = random.choice(statuses)
        if status == 'TP':
            result = round(random.uniform(50, 500), 2)
        elif status == 'SL':
            result = round(random.uniform(-500, -50), 2)
        else:  # BE
            result = round(random.uniform(-20, 20), 2)
        
        # Emotions (0 a 3 emotions)
        num_emotions = random.randint(0, 3)
        emotions = random.sample(emotions_list, num_emotions) if num_emotions > 0 else []
        
        # Confirmations (0 a 4 confirmations)
        num_confirmations = random.randint(0, 4)
        confirmations = random.sample(confirmations_list, num_confirmations) if num_confirmations > 0 else []
        
        # Notes (algunos con, algunos sin)
        notes = random.choice(notes_samples)
        
        # Trading link (algunos con, algunos sin)
        trading_link = random.choice(trading_links)
        
        trades[str(i)] = {
            "id": str(i),
            "symbol": symbol,
            "side": side,
            "rate": rate,
            "risk": risk,
            "result": result,
            "status": status,
            "date": trade_date.isoformat(),
            "notes": notes,
            "emotions": emotions,
            "confirmations": confirmations,
            "trading_link": trading_link
        }
    
    return trades

TRADE_MOCK_DATA = generate_trade_mocks()
