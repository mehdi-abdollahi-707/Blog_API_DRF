from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('posts/' , views.PostListView.as_view() , name='post_list'),
    path('post/<int:pk>/' , views.PostDetailView.as_view() , name='post_detail'),
    path('create/' , views.PostCreateView.as_view() , name='post_create'),
    path('update/<int:pk>/' , views.PostUpdateView.as_view() , name='post_update'),
    path('delete/<int:pk>/' , views.PostDeleteView.as_view() , name='post_delete'),
    path('upload/image/<int:pk>/' , views.PostImageUploadView.as_view() , name='post_image_upload'),
    path('delete/image/<int:pk>/' , views.PostImageDeleteView.as_view() , name='post_image_delete'),
    path('comment/create/<int:pk>/' , views.CommentCreateView.as_view() , name='comment_create'),
    path('comment/update/<int:pk>/' , views.CommentUpdateView.as_view() , name='comment_update'),
]