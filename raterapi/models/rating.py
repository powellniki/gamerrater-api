from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="rating")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating")
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])