from rest_framework import serializers
from .models import User, Post, Attitue


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'username', 'content', 'create_time', 'like', 'hate')


class AttitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attitue
        fields = ('id', 'username', 'pid', 'attitude')
