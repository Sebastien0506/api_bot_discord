from django.db import models

class Reglement(models.Model) :
    user_id = models.CharField(max_length=50, unique=True)
    date_join = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=False)
    dernier_rappel = models.DateTimeField(null=True, blank=True)
