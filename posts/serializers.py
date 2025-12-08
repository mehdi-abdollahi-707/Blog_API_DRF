from rest_framework import serializers
from .models import PostImage , Post , Comment
from django.utils.text import slugify


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user' , 'title' , 'body')





class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        result = obj.images.all()
        return PostImageSerializer(instance=result, many=True).data

    def get_comments(self, obj):
        result = obj.comments.all()
        comments = []
        for c in result:
            if c.parent is None:
                comments.append(c)
        return CommentSerializer(instance=comments, many=True).data


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



class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('post' , 'user' , 'body' ,'replies')

    def get_replies(self, obj):
        result = obj.replies.all()
        return ReplySerializer(instance=result, many=True).data



class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)

    def create(self , validated_data):
        new_comment = Comment(**validated_data)
        new_comment.post = self.context['post']
        new_comment.user = self.context['user']
        new_comment.save()
        return new_comment

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post','user','body')



class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)

    def create(self , validated_data):
        new_comment = Comment(**validated_data)
        new_comment.post = self.context['post']
        new_comment.user = self.context['user']
        new_comment.parent = self.context['comment']
        new_comment.save()
        return new_comment

