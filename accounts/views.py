from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated , AllowAny



class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny(),]
        if self.action in ['retrieve','partial_update','destroy']:
            return [IsAuthenticated(),]

    def create(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
        return Response(srz_data.data , status=status.HTTP_201_CREATED)

    def retrieve(self , request , pk=None):
        user = get_object_or_404(User , pk=pk)
        if request.user == user:
            srz_data = self.serializer_class(instance=user)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response({'message' : 'You are not the owner'})

    def partial_update(self , request , pk=None):
        user = get_object_or_404(User, pk=pk)
        if request.user == user:
            srz_data = self.serializer_class(instance=user , data=request.data , partial=True)
            if srz_data.is_valid():
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_202_ACCEPTED)
            return Response(srz_data.errors , status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : 'You are not the owner'})

    def destroy(self , request , pk=None):
        user = get_object_or_404(User, pk=pk)
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message' : 'You are not the owner'})