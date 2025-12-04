from rest_framework import serializers
from .models import PostImage , Post
from django.template.defaultfilters import slugify
import random


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title' , 'body' , 'status')

    def create(self, validated_data):
        title = validated_data['title']
        validated_data['slug'] = slugify(title)
        return Post.objects.create(**validated_data)

    def validate_title(self, value):
        if Post.objects.filter(title__icontains=value).exists():
            random_code = random.randint(1,10000000)
            value = f'{value} - ({random_code})'
            return value
        return value

