from typing import Dict, List

from app.services.trade_service import trade_service


class TradeStatsService:
    def compute_total_trades(self) -> int:
        return trade_service.get_count()

    def compute_total_pnl(self, trades: List[Dict]) -> float:
        total = 0.0
        for trade in trades:
            result = trade.get("result")
            if result is None:
                continue
            try:
                total += float(result)
            except Exception:
                pass
            
        return total

    def compute_winning_trades(self, trades: List[Dict]) -> int:
        return sum(1 for t in trades if t.get("status") == "TP")

    def compute_losing_trades(self, trades: List[Dict]) -> int:
        return sum(1 for t in trades if t.get("status") == "SL")

    def compute_avg_pnl(self, total_pnl: float, total_trades: int) -> float:
        return (total_pnl / total_trades) if total_trades > 0 else 0.0

    def compute_win_rate(self, winning_trades: int, total_trades: int) -> float:
        return (winning_trades / total_trades * 100.0) if total_trades > 0 else 0.0

    def get_summary(self) -> Dict:
        total_trades = self.compute_total_trades()
        trades_data = trade_service.get_all()

        if not trades_data:
            return {
                "total_trades": 0,
                "total_pnl": 0,
                "avg_pnl": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
            }

        total_pnl = self.compute_total_pnl(trades_data)
        winning_trades = self.compute_winning_trades(trades_data)
        losing_trades = self.compute_losing_trades(trades_data)
        avg_pnl = self.compute_avg_pnl(total_pnl, total_trades)
        win_rate = self.compute_win_rate(winning_trades, total_trades)

        return {
            "total_trades": total_trades,
            "total_pnl": round(total_pnl, 2),
            "avg_pnl": round(avg_pnl, 2),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
        }


trade_stats_service = TradeStatsService()
