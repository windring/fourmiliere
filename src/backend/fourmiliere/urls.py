from django.urls import path, include
from . import views
from rest_framework import routers


routers = routers.DefaultRouter()
routers.register('fourmiliere', views.UserView)


urlpatterns = [
    path('', include(routers.urls)),
    path('signup', views.UserView.sign_up),
    path('signin', views.UserView.sign_in, name="sign_in"),
]
