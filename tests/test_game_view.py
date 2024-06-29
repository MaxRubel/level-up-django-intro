from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.views.game import GameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['gamers', 'game_types', "game"]
    
    def setUp(self):
        self.gamer = Gamer.objects.first()
        self.game = Game.objects.first()

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skillLevel": 5,
            "numberOfPlayers": 6,
            "gameType": 1,
            "userId": 1
        }

        response = self.client.post(url, game, format='json')

        new_game = Game.objects.last()

        expected = GameSerializer(new_game)

        self.assertEqual(expected.data, response.data)

    def test_get_game(self):
        """Get Game Test
        """
        game = Game.objects.first()
        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = GameSerializer(game)

        self.assertEqual(expected.data, response.data)

    def test_list_games(self):
        """Test list games"""
        url = '/games'

        response = self.client.get(url)
        
        all_games = Game.objects.all()
        expected = GameSerializer(all_games, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_game(self):
        """test update game"""

        game = Game.objects.first()

        url = f'/games/{game.id}'

        updated_game = {
            "title": f'{game.title} updated',
            "maker": game.maker,
            "skillLevel": game.skill_level,
            "numberOfPlayers": game.number_of_players,
            "gameType": game.game_type.id,
        }

        response = self.client.put(url, updated_game, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        game.refresh_from_db()

        self.assertEqual(updated_game['title'], game.title)

    def test_delete_game(self):
        """Test delete game"""
        game = Game.objects.first()

        url = f'/games/{game.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)