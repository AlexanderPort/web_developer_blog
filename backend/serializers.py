from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'pk',
            'name',
            'surname',
            'email',
            'description',
            'password',
            'login',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            'pk',
            'name',
            'description',
        ]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            'pk',
            'author_id',
            'title',
            'description',
            'text',
            'created_at',
        ]

class ArticleMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            'pk',
            'author_id',
            'title',
            'description',
            'created_at',
            'likes',
            'dislikes',
            'views',
        ]