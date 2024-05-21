"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event_gamer

class EventGamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event_gamer
        fields = ('id', 'label')

class EventGamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            event_gamer = Event_gamer.objects.get(pk=pk)
            serializer = EventGamerSerializer(event_gamer)
            return Response(serializer.data)
        except Event_gamer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        event_gamers = Event_gamer.objects.all()
        serializer = EventGamerSerializer(event_gamers, many=True)
        return Response(serializer.data)
