from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="pictures")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    picture = models.URLField()