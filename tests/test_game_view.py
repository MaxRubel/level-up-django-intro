from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.views.game import GameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['gamers', 'game_types',]
    
    def setUp(self):
        # Grab the first Gamer object from the database
        self.gamer = Gamer.objects.first()

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skillLevel": 5,
            "numberOfPlayers": 6,
            "gameType": 1,
            "userId": 1
        }

        response = self.client.post(url, game, format='json')

        
        # Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = GameSerializer(new_game)

        # Now we can test that the expected ouput matches what was actually returned
        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        self.assertEqual(expected.data, response.data)