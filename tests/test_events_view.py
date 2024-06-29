from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer, Event
from levelupapi.views.game import GameSerializer
from levelupapi.views.event import EventSerializer

class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['events', 'gamers', 'game', 'game_types', 'event_gamer']
    
    def setUp(self):
        self.event = Event.objects.first()

    def test_create_event(self):
        """Create game test"""
        url = "/events"

        event = {
            "gameId": 1,
            "description": "this is a test event",
            "date": "2024-06-15",
            "time": "14:30:00",
            "gamerId":1,
            "attendees": [1]
        }

        response = self.client.post(url, event, format='json')

        new_event = Event.objects.last()

        expected = EventSerializer(new_event)

        self.assertEqual(expected.data, response.data)

    def test_get_event(self):
        event = Event.objects.first()
        url = f'/events/{event.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_data = EventSerializer(event).data
        
        expected_data['attendees_count'] = 1 

        self.assertEqual(expected_data, response.data)

    def test_list_events(self):
        """Test list games"""

        url = '/events'
        
        self.client.credentials(HTTP_AUTHORIZATION='1')
        
        response = self.client.get(url)
        
        all_events = Event.objects.all()
        expected = EventSerializer(all_events, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_event(self):
        """test update game"""

        event = Event.objects.first()

        url = f'/events/{event.id}'

        updated_event = {
            "gameId": 1,
            "description": "this is an updated event",
            "date": "2024-06-15",
            "time": "14:30:00",
            "gamerId":1,
            "attendees": [1]
        }

        response = self.client.put(url, updated_event, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        event.refresh_from_db()

        self.assertEqual(updated_event['description'], event.description)

    def test_delete_event(self):
        """Test delete game"""
        event = Event.objects.first()

        url = f'/events/{event.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)