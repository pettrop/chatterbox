from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars


# Create your models here.
class Room(Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True) # null => dovoluje prazdny popisok; blank => dovoluje prazdny znaky
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # blank dovoli aby miestnost bola prazdna
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', 'name'] # bez minuska pred created je radenie od najstarsej po najnovsiu miestnost, minusko otoci radenie


class Message(Model):
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def body_short(self):
        return truncatechars(self.body, 50)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-created', 'body']
