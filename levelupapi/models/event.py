from django.db import models
from .game import Game
from .gamer import Gamer

class Event (models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Gamer, through='EventGamer', related_name='gamers')

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value