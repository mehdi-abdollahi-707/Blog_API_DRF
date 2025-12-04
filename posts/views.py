from django.shortcuts import render
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.views import APIView
from .models import Post
from rest_framework import status



class PostListView(APIView):
    serializer_class = PostSerializer

    def get(self , request):
        posts = Post.objects.all()
        srz_data = self.serializer_class(instance=posts, many=True)
        return Response(data= srz_data.data , status=status.HTTP_200_OK)