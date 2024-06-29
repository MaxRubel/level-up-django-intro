"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Gamer
        fields = ('id','uid', 'bio')

class GamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(game_type)
            return Response(serializer.data)
        except Gamer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        gamer = Gamer.objects.get(pk=pk)
        gamer.uid=request.data["uid"]
        gamer.bio=request.data["bio"]
        gamer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        game_types = Gamer.objects.all()
        serializer = GamerSerializer(game_types, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        gamer = Gamer.objects.create(
            uid = request.data["uid"],
            bio = request.data["bio"]
        )
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)

    def destroy(self, request, pk):
        gamer = Gamer.objects.get(pk=pk)
        gamer.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
