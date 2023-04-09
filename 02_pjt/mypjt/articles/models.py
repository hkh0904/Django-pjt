from django.db import models
# Create your models here.
class Articles(models.Model):
    author = models.CharField(max_length=20)
    comment = models.TextField()
    rate = models.IntegerField()
    board_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
