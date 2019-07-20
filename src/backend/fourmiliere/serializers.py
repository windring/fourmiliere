from rest_framework import serializers
from .models import User, Post, Like, Hate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'username', 'content', 'create_time', 'like', 'hate')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'username', 'pid')


class HateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hate
        fields = ('id', 'username', 'pid')