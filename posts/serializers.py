from rest_framework import serializers
from .models import PostImage , Post
from django.utils.text import slugify



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'




class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')

    def create(self, validated_data):
        title = validated_data['title']
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        # Make slug unique
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data['slug'] = slug
        return Post.objects.create(**validated_data)


