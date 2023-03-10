from django.urls import path
from .views import (PostDetail, PostsHome,
                    GroupPosts, Profile,
                    CommentCreateView,
                    CreatePostView,
                    PostDeleteView,
                    PostEditView, FollowView,
                    AddFollowView, UnfollowView)

app_name = 'posts'

urlpatterns = [
    path('', PostsHome.as_view(), name='index'),
    path('group/<slug:group_slug>/', GroupPosts.as_view(), name='group_list'),
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('create/', CreatePostView.as_view(), name='post_create'),
    path('posts/<post_id>/edit/', PostEditView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/delete/<int:pk>', PostDeleteView.as_view(),
         name='delete_post'),
    path('follow/', FollowView.as_view(), name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        AddFollowView.as_view(),
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        UnfollowView.as_view(),
        name='profile_unfollow'
    ),
]
