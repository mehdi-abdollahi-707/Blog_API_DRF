from rest_framework import serializers
from .models import PostImage , Post



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

