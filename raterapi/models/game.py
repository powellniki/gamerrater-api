from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    designer = models.CharField(max_length=50)
    release_year = models.IntegerField()
    number_players = models.IntegerField()
    play_time = models.CharField(max_length=100)
    age_rec = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')