from rest_framework.response import Response
from .serializers import PostSerializer , PostCreateSerializer
from rest_framework.views import APIView
from .models import Post
from rest_framework import status
from django.shortcuts import get_object_or_404
from permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated







class PostListView(APIView):
    serializer_class = PostSerializer

    def get(self , request):
        posts = Post.objects.all()
        srz_data = self.serializer_class(instance=posts, many=True)
        return Response(data= srz_data.data , status=status.HTTP_200_OK)


class PostDetailView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        post = get_object_or_404(Post , pk=pk)
        srz_data = self.serializer_class(instance=post)
        return Response(data= srz_data.data , status=status.HTTP_200_OK)


class PostCreateView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(self.serializer_class(post).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

