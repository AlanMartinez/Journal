"""
Tests unitarios para las rutas de emotions
"""
import pytest
from unittest.mock import patch

from tests.conftest import client


class TestEmotionsRoutes:
    """Tests para los endpoints de emotions"""

    @patch('app.routes.emotions.emotion_service')
    def test_get_all_emotions(self, mock_service, client):
        """Test para obtener todas las emotions"""
        mock_data = [
            {
                'id': '1',
                'name': 'Frustration',
                'description': 'Feeling frustrated'
            },
            {
                'id': '2',
                'name': 'Confidence',
                'description': 'Feeling confident'
            }
        ]
        mock_service.get_all.return_value = mock_data
        
        response = client.get("/emotions/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == 'Frustration'
        assert data[1]['name'] == 'Confidence'

    @patch('app.routes.emotions.emotion_service')
    def test_get_all_emotions_empty(self, mock_service, client):
        """Test para obtener emotions cuando no hay datos"""
        mock_service.get_all.return_value = []
        
        response = client.get("/emotions/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert isinstance(data, list)

    @patch('app.routes.emotions.emotion_service')
    def test_create_emotion(self, mock_service, client):
        """Test para crear una nueva emotion"""
        new_emotion = {
            'id': 'new-id',
            'name': 'Anxiety',
            'description': 'Feeling anxious about the trade'
        }
        mock_service.create.return_value = new_emotion
        
        payload = {
            'name': 'Anxiety',
            'description': 'Feeling anxious about the trade'
        }
        
        response = client.post("/emotions/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'new-id'
        assert data['name'] == 'Anxiety'
        assert data['description'] == 'Feeling anxious about the trade'
        mock_service.create.assert_called_once()

    @patch('app.routes.emotions.emotion_service')
    def test_create_emotion_minimal(self, mock_service, client):
        """Test para crear una emotion con campos mínimos"""
        new_emotion = {
            'id': 'new-id',
            'name': 'Happy'
        }
        mock_service.create.return_value = new_emotion
        
        payload = {
            'name': 'Happy'
        }
        
        response = client.post("/emotions/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Happy'

    @patch('app.routes.emotions.emotion_service')
    def test_delete_emotion(self, mock_service, client):
        """Test para eliminar una emotion"""
        deleted_emotion = {
            'id': '1',
            'name': 'Frustration'
        }
        mock_service.delete.return_value = deleted_emotion
        
        response = client.delete("/emotions/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data['message'].lower()
        assert data['deleted_emotion']['id'] == '1'
        assert data['deleted_emotion']['name'] == 'Frustration'

    @patch('app.routes.emotions.emotion_service')
    def test_delete_emotion_not_found(self, mock_service, client):
        """Test para eliminar una emotion inexistente"""
        mock_service.delete.return_value = None
        
        response = client.delete("/emotions/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()['detail'].lower()

    def test_emotion_validation(self, client):
        """Test para validar campos requeridos al crear una emotion"""
        payload = {
            'description': 'Some description'
            # Falta 'name' que es requerido
        }
        
        response = client.post("/emotions/", json=payload)
        
        assert response.status_code == 422  # Validation error

