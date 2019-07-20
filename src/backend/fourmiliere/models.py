from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum, unique


@unique
class ATTITUTE(Enum):
    HATE = -1
    LIKE = 1
    UNDE = 0


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=2000)
    create_time = models.BigIntegerField()
    like = models.IntegerField()
    hate = models.IntegerField()


class Attitude(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    pid = models.ForeignKey('Post', on_delete=models.CASCADE, to_field='id')
    attitude = models.IntegerField()

