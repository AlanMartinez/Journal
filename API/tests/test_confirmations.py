"""
Tests unitarios para las rutas de confirmations
"""
import pytest
from unittest.mock import patch

from tests.conftest import client


class TestConfirmationsRoutes:
    """Tests para los endpoints de confirmations"""

    @patch('app.routes.confirmations.confirmation_service')
    def test_get_all_confirmations(self, mock_service, client):
        """Test para obtener todas las confirmations"""
        mock_data = [
            {
                'id': '1',
                'name': 'Volume Spike',
                'description': 'Volume increased significantly'
            },
            {
                'id': '2',
                'name': 'Support Level',
                'description': 'Price bounced from support'
            }
        ]
        mock_service.get_all.return_value = mock_data
        
        response = client.get("/confirmations/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == 'Volume Spike'
        assert data[1]['name'] == 'Support Level'

    @patch('app.routes.confirmations.confirmation_service')
    def test_get_all_confirmations_empty(self, mock_service, client):
        """Test para obtener confirmations cuando no hay datos"""
        mock_service.get_all.return_value = []
        
        response = client.get("/confirmations/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert isinstance(data, list)

    @patch('app.routes.confirmations.confirmation_service')
    def test_create_confirmation(self, mock_service, client):
        """Test para crear una nueva confirmation"""
        new_confirmation = {
            'id': 'new-id',
            'name': 'Trend Line Break',
            'description': 'Price broke through trend line'
        }
        mock_service.create.return_value = new_confirmation
        
        payload = {
            'name': 'Trend Line Break',
            'description': 'Price broke through trend line'
        }
        
        response = client.post("/confirmations/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'new-id'
        assert data['name'] == 'Trend Line Break'
        assert data['description'] == 'Price broke through trend line'
        mock_service.create.assert_called_once()

    @patch('app.routes.confirmations.confirmation_service')
    def test_create_confirmation_minimal(self, mock_service, client):
        """Test para crear una confirmation con campos mínimos"""
        new_confirmation = {
            'id': 'new-id',
            'name': 'RSI Oversold'
        }
        mock_service.create.return_value = new_confirmation
        
        payload = {
            'name': 'RSI Oversold'
        }
        
        response = client.post("/confirmations/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'RSI Oversold'

    @patch('app.routes.confirmations.confirmation_service')
    def test_delete_confirmation(self, mock_service, client):
        """Test para eliminar una confirmation"""
        deleted_confirmation = {
            'id': '1',
            'name': 'Volume Spike'
        }
        mock_service.delete.return_value = deleted_confirmation
        
        response = client.delete("/confirmations/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data['message'].lower()
        assert data['deleted_confirmation']['id'] == '1'
        assert data['deleted_confirmation']['name'] == 'Volume Spike'

    @patch('app.routes.confirmations.confirmation_service')
    def test_delete_confirmation_not_found(self, mock_service, client):
        """Test para eliminar una confirmation inexistente"""
        mock_service.delete.return_value = None
        
        response = client.delete("/confirmations/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()['detail'].lower()

    def test_confirmation_validation(self, client):
        """Test para validar campos requeridos al crear una confirmation"""
        payload = {
            'description': 'Some description'
            # Falta 'name' que es requerido
        }
        
        response = client.post("/confirmations/", json=payload)
        
        assert response.status_code == 422  # Validation error

