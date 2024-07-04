from django.db import models

from django.contrib.auth.models import User
from comments.models import Comment

VOTE_DIRECTION = ((0, 'neutral'), (1, 'up'), (2, 'down'))

class Vote(models.Model):
    """
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_together' makes sure a user can't like the same post twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name='votes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    direction = models.IntegerField(choices=VOTE_DIRECTION, default=0)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'comment']

    def __str__(self):
        return f'{self.owner} {self.direction} vote on {self.comment}'