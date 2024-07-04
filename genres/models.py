from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False)
    color = models.SlugField(max_length=7, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'