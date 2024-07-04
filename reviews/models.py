from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator 

RATING = ((0, "0 stars"), (1, "1 star"), (2, "2 stars"), (3, "3 stars"), (4, "4 stars"), (5, "5 stars"))



class Review(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    rating = models.IntegerField(default=3, choices=RATING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} reviews {self.movie.title}'