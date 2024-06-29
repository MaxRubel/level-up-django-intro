from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Gamer
from levelupapi.views.gamer import GamerSerializer

class GamerTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['gamers']
    
    def setUp(self):
        self.gamer = Gamer.objects.first()

    def test_create_gamer(self):
        """Create game test"""
        url = "/gamers"

        gamer = {
            "uid": 2,
            "bio": "Me"
        }

        response = self.client.post(url, gamer, format='json')

        new_gamer = Gamer.objects.last()

        expected = GamerSerializer(new_gamer)

        self.assertEqual(expected.data, response.data)

    def test_get_game(self):
        """Get Game Test
        """
        gamer = Gamer.objects.first()
        url = f'/gamers/{gamer.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = GamerSerializer(gamer)

        self.assertEqual(expected.data, response.data)

    def test_list_games(self):
        """Test list games"""
        url = '/gamers'

        response = self.client.get(url)
        
        all_gamers = Gamer.objects.all()
        expected = GamerSerializer(all_gamers, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_gamer(self):
        """test update game"""

        gamer = Gamer.objects.first()

        url = f'/gamers/{gamer.id}'

        updated_gamer = {
            "uid": 2,
            "bio": "Me updated"
        }

        response = self.client.put(url, updated_gamer, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        gamer.refresh_from_db()

        self.assertEqual(updated_gamer['bio'], gamer.bio)

    def test_delete_gamer(self):
        """Test delete game"""
        gamer = Gamer.objects.first()

        url = f'/gamers/{gamer.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)