from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    designer = models.CharField(max_length=50)
    release_year = models.IntegerField()
    number_players = models.CharField(max_length=50)
    play_time = models.CharField(max_length=50)
    age_rec = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = self.rating.all()

        # Sum all of the ratings for the game
        total_rating = sum(rating.rating for rating in ratings)
        
        # Calculate the average and return it
        if ratings.exists():
            average_rating = total_rating / ratings.count()
        else:
            average_rating = 0

        return average_rating