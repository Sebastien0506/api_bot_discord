from django.db import models

class Reglement(models.Model) :
    user_id = models.CharField(max_length=50, unique=True)
    date_join = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=False)
    dernier_rappel = models.DateTimeField(null=True, blank=True)

from django.db import models


class PendingAction(models.Model):
    ACTION_CHOICES = [
        ("join_voice", "Join voice channel"),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    channel_id = models.BigIntegerField()
    user_id = models.BigIntegerField()

    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} | guild={self.channel_id} | user={self.user_id}"