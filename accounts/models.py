from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES=(
        ('M', '남성'),
        ('F', '여성'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(blank=True, null=True)
    weekly_avg_reading_time = models.PositiveIntegerField(blank = True, null = True)
    yearly_read_count=models.PositiveIntegerField(blank = True, null = True)
    profile = models.ImageField(upload_to='',default='base_image.png',blank=True)
    category = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='카테고리',
        )
    
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

# class UserFollowings(models.Model):
#     from_user_id=models.ForeignKey(User, on_delete=models.CASCADE)
#     to_user_id=models.ForeignKey(User, on_delete=models.CASCADE)