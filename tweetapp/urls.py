from django.urls import path
from . import views


urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('tweets/search/', views.search_tweet_list, name='search_tweet_list'),
     path('tweet/<int:tweet_id>/comment/', views.comment_create, name='comment_create'),
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),

]