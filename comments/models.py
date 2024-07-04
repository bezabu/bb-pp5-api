from django.db import models
from django.contrib.auth.models import User
from reviews.models import Review


class Comment(models.Model):
    """
    Comment model, related to User and Review
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content