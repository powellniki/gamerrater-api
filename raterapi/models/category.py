from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    game = models.ManyToManyField("Game", through="GameCategories", related_name="categories")