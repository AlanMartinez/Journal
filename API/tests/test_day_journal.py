"""
Tests unitarios para las rutas de day_journal
"""
import pytest
from datetime import date
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from tests.conftest import client, day_journal_service_mock
from app.models.day_journal import DayJournalCreate, DayJournalUpdate


class TestDayJournalRoutes:
    """Tests para los endpoints de day_journal"""

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_all_day_journals(self, mock_service, client):
        """Test para obtener todos los day_journals"""
        # Mock data
        mock_data = [
            {
                'id': '1',
                'date': '2024-01-15',
                'break_trading_plan': False,
                'notes': 'Test note 1'
            },
            {
                'id': '2',
                'date': '2024-01-16',
                'break_trading_plan': True,
                'notes': 'Test note 2'
            }
        ]
        mock_service.get_all.return_value = mock_data
        
        # Realizar request
        response = client.get("/day-journal/")
        
        # Verificar respuesta
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['id'] == '1'
        assert data[1]['id'] == '2'

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_all_day_journals_with_pagination(self, mock_service, client):
        """Test para obtener day_journals con paginación"""
        mock_data = [
            {'id': str(i), 'date': f'2024-01-{i:02d}', 'break_trading_plan': False}
            for i in range(1, 6)
        ]
        mock_service.get_all.return_value = mock_data
        
        response = client.get("/day-journal/?skip=0&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_all_day_journals_no_slash(self, mock_service, client):
        """Test para obtener day_journals sin barra final"""
        mock_data = [
            {'id': '1', 'date': '2024-01-15', 'break_trading_plan': False}
        ]
        mock_service.get_all.return_value = mock_data
        
        response = client.get("/day-journal")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_day_journal_by_id(self, mock_service, client):
        """Test para obtener un day_journal por ID"""
        mock_data = {
            'id': '1',
            'date': '2024-01-15',
            'break_trading_plan': False,
            'notes': 'Test note'
        }
        mock_service.get_by_id.return_value = mock_data
        
        response = client.get("/day-journal/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == '1'
        assert data['date'] == '2024-01-15'

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_day_journal_by_id_not_found(self, mock_service, client):
        """Test para obtener un day_journal inexistente"""
        mock_service.get_by_id.return_value = None
        
        response = client.get("/day-journal/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()['detail'].lower()

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_day_journals_by_date_range(self, mock_service, client):
        """Test para obtener day_journals por rango de fechas"""
        mock_data = [
            {'id': '1', 'date': '2024-01-15', 'break_trading_plan': False},
            {'id': '2', 'date': '2024-01-16', 'break_trading_plan': False}
        ]
        mock_service.get_by_date_range.return_value = mock_data
        
        response = client.get("/day-journal/range?start_date=2024-01-15&end_date=2024-01-16")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @patch('app.routes.day_journal.day_journal_service')
    def test_get_day_journals_by_date_range_invalid(self, mock_service, client):
        """Test para obtener day_journals con rango de fechas inválido"""
        response = client.get("/day-journal/range?start_date=2024-01-16&end_date=2024-01-15")
        
        assert response.status_code == 400
        assert "start_date" in response.json()['detail'].lower()

    @patch('app.routes.day_journal.day_journal_service')
    def test_create_day_journal(self, mock_service, client):
        """Test para crear un nuevo day_journal"""
        new_day_journal = {
            'id': 'new-id',
            'date': '2024-01-20',
            'break_trading_plan': False,
            'notes': 'New journal entry'
        }
        mock_service.create.return_value = new_day_journal
        
        payload = {
            'date': '2024-01-20',
            'break_trading_plan': False,
            'notes': 'New journal entry'
        }
        
        response = client.post("/day-journal/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'new-id'
        assert data['date'] == '2024-01-20'
        assert data['notes'] == 'New journal entry'
        mock_service.create.assert_called_once()

    @patch('app.routes.day_journal.day_journal_service')
    def test_create_day_journal_no_slash(self, mock_service, client):
        """Test para crear day_journal sin barra final"""
        new_day_journal = {
            'id': 'new-id',
            'date': '2024-01-20',
            'break_trading_plan': False
        }
        mock_service.create.return_value = new_day_journal
        
        payload = {
            'date': '2024-01-20',
            'break_trading_plan': False
        }
        
        response = client.post("/day-journal", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'new-id'

    @patch('app.routes.day_journal.day_journal_service')
    def test_update_day_journal(self, mock_service, client):
        """Test para actualizar un day_journal existente"""
        updated_day_journal = {
            'id': '1',
            'date': '2024-01-15',
            'break_trading_plan': True,
            'notes': 'Updated note'
        }
        mock_service.update.return_value = updated_day_journal
        
        payload = {
            'break_trading_plan': True,
            'notes': 'Updated note'
        }
        
        response = client.put("/day-journal/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['break_trading_plan'] is True
        assert data['notes'] == 'Updated note'

    @patch('app.routes.day_journal.day_journal_service')
    def test_update_day_journal_not_found(self, mock_service, client):
        """Test para actualizar un day_journal inexistente"""
        mock_service.update.return_value = None
        
        payload = {
            'break_trading_plan': True
        }
        
        response = client.put("/day-journal/999", json=payload)
        
        assert response.status_code == 404
        assert "not found" in response.json()['detail'].lower()

    @patch('app.routes.day_journal.day_journal_service')
    def test_update_day_journal_partial(self, mock_service, client):
        """Test para actualizar solo algunos campos"""
        updated_day_journal = {
            'id': '1',
            'date': '2024-01-15',
            'break_trading_plan': True,
            'notes': 'Original note'
        }
        mock_service.update.return_value = updated_day_journal
        
        payload = {
            'break_trading_plan': True
        }
        
        response = client.put("/day-journal/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['break_trading_plan'] is True

    @patch('app.routes.day_journal.day_journal_service')
    def test_delete_day_journal(self, mock_service, client):
        """Test para eliminar un day_journal"""
        deleted_day_journal = {
            'id': '1',
            'date': '2024-01-15',
            'break_trading_plan': False
        }
        mock_service.delete.return_value = deleted_day_journal
        
        response = client.delete("/day-journal/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data['message'].lower()
        assert data['deleted_day_journal']['id'] == '1'

    @patch('app.routes.day_journal.day_journal_service')
    def test_delete_day_journal_not_found(self, mock_service, client):
        """Test para eliminar un day_journal inexistente"""
        mock_service.delete.return_value = None
        
        response = client.delete("/day-journal/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()['detail'].lower()

    @patch('app.routes.day_journal.day_journal_service')
    def test_date_string_conversion(self, mock_service, client):
        """Test para verificar conversión correcta de fechas como string"""
        mock_data = {
            'id': '1',
            'date': '2024-01-15',  # String date
            'break_trading_plan': False
        }
        mock_service.get_by_id.return_value = mock_data
        
        response = client.get("/day-journal/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data['date'] == '2024-01-15'  # FastAPI serializa date a string

    def test_day_journal_validation(self, client):
        """Test para validar que se requiere la fecha al crear"""
        payload = {
            'break_trading_plan': False
            # Falta 'date' que es requerido
        }
        
        response = client.post("/day-journal/", json=payload)
        
        assert response.status_code == 422  # Validation error

