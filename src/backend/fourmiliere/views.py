from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def sign_up(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        if username is not None and password is not None:
            try:
                user = User.objects.create_user(username=username,
                                                password=password)
                return JsonResponse({'username': user.username},
                                    status=status.HTTP_200_OK,
                                    safe=False)
            except Exception as e:
                return JsonResponse({'error': str(e)},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False)
        return JsonResponse({'error': 'bad request'},
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

    def sign_in(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(request=request,
                            nickname=username,
                            password=password)
        if not user:
            return JsonResponse({'username': username},
                                status=status.HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse({},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False)


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def new_post(request):
        if request.user.is_authenticated:
            post = PostSerializer(request.GET)
            post.save()
            return JsonResponse({'message': '发布成功'},
                                status=status.HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse({'error': '发布失败'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False)

    def like(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False)
        try:
            pid = request.GET.get('pid')
            post = Post.objects.filter(id=pid)
            post.like += 1
            post.save()
            return JsonResponse({'message': '完成'},
                                status=status.HTTP_200_OK,
                                safe=False)
        except Exception as e:
            return JsonResponse({'error', str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False)

    def hate(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False)
        try:
            pid = request.GET.get('pid')
            post = Post.objects.filter(id=pid)
            post.hate += 1
            post.save()
            return JsonResponse({'message': '完成'},
                                status=status.HTTP_200_OK,
                                safe=False)
        except Exception as e:
            return JsonResponse({'error', str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False)
