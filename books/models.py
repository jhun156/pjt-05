from django.db import models
from django.conf import settings

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    customer_review_rank = models.IntegerField()
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(blank=True)
    author_profile_img = models.ImageField(blank=True)
    author_info = models.TextField()
    author_works = models.TextField()
    audio_file = models.FileField(blank=True, upload_to='audio/')


class Thread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    reading_date = models.DateField()
    cover_img = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 추가한 내용
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_threads')