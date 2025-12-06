from rest_framework import serializers
from .models import PostImage , Post
from django.utils.text import slugify



class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        result = obj.images.all()
        return PostImageSerializer(instance=result, many=True).data


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



class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')

    def update(self, instance, validated_data):
        # Update fields
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)

        # Update slug if title changed
        if 'title' in validated_data:
            title = validated_data['title']
            base_slug = slugify(title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exclude(id=instance.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            instance.slug = slug

        instance.save()
        return instance


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id' , 'image')








