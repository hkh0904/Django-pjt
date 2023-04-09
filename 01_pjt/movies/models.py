from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateField()
    genre_choices = (('Comedy', 'Comedy'), ('Thriller', 'Thriller'), ('Romance', 'Romance'))
    genre = models.CharField(max_length=30, choices=genre_choices, default='Comedy')
    score = models.FloatField()
    poster_url = models.CharField(max_length=50)
    description = models.TextField()
    actor_image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.title