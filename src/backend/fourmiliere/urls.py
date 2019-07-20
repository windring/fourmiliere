from django.urls import path, include
from . import views
from rest_framework import routers


routers = routers.DefaultRouter()
routers.register('fourmiliere', views.UserView)
routers.register('fourmiliere', views.PostView)


urlpatterns = [
    # path('', include(routers.urls)),
    path('user/signup/', views.UserView.sign_up),
    path('user/signin/', views.UserView.sign_in),
    path('user/auth/', views.UserView.is_login),
    path('user/signout/', views.UserView.sign_out),
    path('post/hate/', views.PostView.hate),
    path('post/like/', views.PostView.like),
    path('post/new/', views.PostView.new_post),
    path('post/all/', views.PostView.all_post),
    path('post/page/', views.PostView.page)
]
