from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=2000)
    create_time = models.BigIntegerField()
    like = models.IntegerField()
    hate = models.IntegerField()


class Hate(models.Model):
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    pid = models.ForeignKey('Post', on_delete=models.CASCADE, to_field='id')


class Like(models.Model):
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    pid = models.ForeignKey('Post', on_delete=models.CASCADE, to_field='id')
