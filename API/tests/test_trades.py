"""
Tests unitarios para las rutas de trades
"""
import pytest
from unittest.mock import patch, AsyncMock
from datetime import date

from tests.conftest import client


class TestTradesRoutes:
    """Tests para los endpoints de trades"""

    @patch('app.routes.trades.trade_service')
    def test_get_all_trades(self, mock_service, client):
        """Test para obtener todos los trades"""
        mock_data = [
            {
                'id': '1',
                'symbol': 'AAPL',
                'side': 'buy',
                'date': '2024-01-15',
                'rate': 150.00,
                'risk': 2.0,
                'result': 500.00,
                'status': 'TP'
            },
            {
                'id': '2',
                'symbol': 'TSLA',
                'side': 'sell',
                'date': '2024-01-16',
                'rate': 200.00,
                'risk': 1.5,
                'result': -250.00,
                'status': 'SL'
            }
        ]
        mock_service.get_all.return_value = mock_data

        response = client.get("/trades/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Los trades se ordenan por fecha descendente (más reciente primero)
        assert data[0]['symbol'] == 'TSLA'  # 2024-01-16 (más reciente)
        assert data[1]['symbol'] == 'AAPL'  # 2024-01-15

    @patch('app.routes.trades.trade_service')
    def test_get_all_trades_empty(self, mock_service, client):
        """Test para obtener trades cuando no hay datos"""
        mock_service.get_all.return_value = []

        response = client.get("/trades/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert isinstance(data, list)

    @patch('app.routes.trades.trade_service')
    def test_get_trade_by_id(self, mock_service, client):
        """Test para obtener un trade por ID"""
        mock_data = {
            'id': '1',
            'symbol': 'AAPL',
            'side': 'buy',
            'date': '2024-01-15',
            'rate': 150.00,
            'risk': 2.0,
            'result': 500.00,
            'status': 'TP'
        }
        mock_service.get_by_id.return_value = mock_data

        response = client.get("/trades/1")

        assert response.status_code == 200
        data = response.json()
        assert data['id'] == '1'
        assert data['symbol'] == 'AAPL'

    @patch('app.routes.trades.trade_service')
    def test_get_trade_by_id_not_found(self, mock_service, client):
        """Test para obtener un trade que no existe"""
        mock_service.get_by_id.return_value = None

        response = client.get("/trades/999")

        assert response.status_code == 404
        assert response.json()['detail'] == "Trade not found"

    @patch('app.routes.trades.trade_service')
    def test_create_trade(self, mock_service, client):
        """Test para crear un nuevo trade - ASYNC"""
        trade_payload = {
            'symbol': 'AAPL',
            'side': 'buy',
            'date': '2024-01-15',
            'rate': 150.00,
            'risk': 2.0,
            'result': 500.00,
            'status': 'TP'
        }

        mock_created_data = {
            'id': '123',
            **trade_payload
        }

        # Mock create_async (ahora es async)
        mock_service.create_async = AsyncMock(return_value=mock_created_data)

        response = client.post("/trades/", json=trade_payload)

        assert response.status_code == 200
        data = response.json()
        assert data['id'] == '123'
        assert data['symbol'] == 'AAPL'
        assert data['rate'] == 150.00
        assert data['result'] == 500.00

        # Verificar que create_async fue llamado
        mock_service.create_async.assert_called_once()

    @patch('app.routes.trades.trade_service')
    def test_create_trade_minimal(self, mock_service, client):
        """Test para crear un trade con datos mínimos"""
        trade_payload = {
            'symbol': 'TSLA',
            'side': 'sell',
            'date': '2024-01-16',
            'rate': 200.00
        }

        mock_created_data = {
            'id': '456',
            **trade_payload
        }

        mock_service.create_async = AsyncMock(return_value=mock_created_data)

        response = client.post("/trades/", json=trade_payload)

        assert response.status_code == 200
        data = response.json()
        assert data['id'] == '456'
        assert data['symbol'] == 'TSLA'

    @patch('app.routes.trades.trade_service')
    def test_update_trade(self, mock_service, client):
        """Test para actualizar un trade existente"""
        update_payload = {
            'rate': 160.00,
            'result': 1000.00
        }

        mock_updated_data = {
            'id': '1',
            'symbol': 'AAPL',
            'side': 'buy',
            'date': '2024-01-15',
            'rate': 160.00,
            'risk': 2.0,
            'result': 1000.00,
            'status': 'TP'
        }

        mock_service.update.return_value = mock_updated_data

        response = client.put("/trades/1", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data['rate'] == 160.00
        assert data['result'] == 1000.00

    @patch('app.routes.trades.trade_service')
    def test_update_trade_not_found(self, mock_service, client):
        """Test para actualizar un trade que no existe"""
        update_payload = {
            'rate': 160.00
        }

        mock_service.update.return_value = None

        response = client.put("/trades/999", json=update_payload)

        assert response.status_code == 404
        assert response.json()['detail'] == "Trade not found"

    @patch('app.routes.trades.trade_service')
    def test_delete_trade(self, mock_service, client):
        """Test para eliminar un trade"""
        mock_deleted_data = {
            'id': '1',
            'symbol': 'AAPL',
            'side': 'buy',
            'date': '2024-01-15',
            'rate': 150.00,
            'risk': 2.0,
            'result': 500.00,
            'status': 'TP'
        }

        mock_service.delete.return_value = mock_deleted_data

        response = client.delete("/trades/1")

        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "Trade deleted successfully"
        assert data['deleted_trade']['id'] == '1'

    @patch('app.routes.trades.trade_service')
    def test_delete_trade_not_found(self, mock_service, client):
        """Test para eliminar un trade que no existe"""
        mock_service.delete.return_value = None

        response = client.delete("/trades/999")

        assert response.status_code == 404
        assert response.json()['detail'] == "Trade not found"

    @patch('app.routes.trades.trade_service')
    def test_trade_validation(self, mock_service, client):
        """Test para validación de datos de trade"""
        # Payload inválido - falta symbol y side
        invalid_payload = {
            'date': '2024-01-15',
            'rate': 150.00
        }

        response = client.post("/trades/", json=invalid_payload)

        # Debería fallar validación
        assert response.status_code == 422
