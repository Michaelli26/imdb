from django.db import models

# Create your models here.


class Movie(models.Model):
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    title = models.CharField(max_length=200)
    rank = models.IntegerField()
    num_votes = models.IntegerField()
    id = models.CharField(max_length=30, primary_key=True)
    year = models.IntegerField()
    runtime = models.IntegerField(null=True)
    weighted_rating = models.FloatField()
    genre = models.CharField(max_length=200, blank=True)
    summary = models.TextField()
    country = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=100, blank=True)
    #trailer = models.URLField()