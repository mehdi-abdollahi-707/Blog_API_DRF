from rest_framework.response import Response
from .serializers import (PostSerializer , PostCreateSerializer ,PostUpdateSerializer,
                          PostListSerializer,CommentCreateSerializer)
from rest_framework.views import APIView
from .models import Post , PostImage , Comment
from rest_framework import status
from django.shortcuts import get_object_or_404
from permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser



class PostListView(APIView):
    serializer_class = PostListSerializer

    def get(self , request):
        posts = Post.objects.filter(status='published')
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



class PostUpdateView(APIView):
    serializer_class = PostUpdateSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self , request , pk):
        post = get_object_or_404(Post , pk=pk)
        srz_data = self.serializer_class(instance=post , data=request.data , partial=True)
        self.check_object_permissions(request,post)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status=status.HTTP_200_OK)
        return Response(srz_data.errors,status=status.HTTP_400_BAD_REQUEST)



class PostDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self , request , pk):
        post = get_object_or_404(Post , pk=pk)
        self.check_object_permissions(request,post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostImageUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if not request.user == post.user:
            return Response({"message" : "You are not the owner"}, status=status.HTTP_401_UNAUTHORIZED)
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "Image is required"}, status=400)
        PostImage.objects.create(post=post, image=image)
        return Response({"message": "Image uploaded"}, status=201)


class PostImageDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self , request , pk):
        image = get_object_or_404(PostImage , pk=pk)
        self.check_object_permissions(request,image.post)
        image.delete()
        return Response({"message": "Image deleted"}, status=status.HTTP_204_NO_CONTENT)


class CommentCreateView(APIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self , request , pk):
        post = get_object_or_404(Post, pk=pk)
        srz_data = self.serializer_class(data=request.data , context={'post':post , 'user':request.user})
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status=status.HTTP_201_CREATED)
        return Response(srz_data.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self , request , pk):
        comment = get_object_or_404(Comment, pk=pk)
        srz_data = self.serializer_class(instance=comment , data=request.data , partial=True)
        self.check_object_permissions(request,comment)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status=status.HTTP_200_OK)
        return Response(srz_data.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self , request , pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request,comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







