"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, EventGamer
from rest_framework.decorators import action
from django.db.models import Count

class EventSerializer(serializers.ModelSerializer):
    attendees_count = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_attendees_count(self, obj):
        return obj.attendees.count()

    def get_joined(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            return user in obj.attendees.all()
        return False

class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for event

        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            event.attendees_count = Event.objects.filter(pk=pk).annotate(attendees_count=Count('attendees')).first().attendees_count
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            


    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.annotate(attendees_count=Count('attendees'))
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)

        for event in events:
            event.joined = len(EventGamer.objects.filter(
                gamer=gamer, event=event)) > 0

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=request.data["gameId"])
        organizer = Gamer.objects.get(pk=request.data["gamerId"])

        event = Event.objects.create(
            game = game,
            description = request.data["description"],  
            date = request.data["date"],
            time = request.data["time"],
            organizer = organizer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["gameId"])
        organizer = Gamer.objects.get(pk=request.data["gamerId"])
        
        event.game = game
        event.organizer = organizer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(id=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
        
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(id=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.get(event_id=event.id, gamer_id=gamer.id)
        attendee.delete()
        return Response({'message': 'Gamer left event'}, status=status.HTTP_201_CREATED)