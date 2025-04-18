from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    customer_review_rank=models.IntegerField()
    author=models.CharField(max_length=100)
    cover_image=models.ImageField(blank=True)