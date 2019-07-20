from django.http import JsonResponse
from rest_framework import viewsets
from .models import User, Post, Attitue
from .models import ATTITUTE
from .serializers import UserSerializer, PostSerializer, AttitudeSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.paginator import Paginator


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
                                    safe=False
                                    )
            except Exception as e:
                return JsonResponse({'error': str(e)},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False
                                    )
        return JsonResponse({'error': 'bad request'},
                            status=status.HTTP_400_BAD_REQUEST, safe=False
                            )

    def sign_in(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request,
                  user
                  )
            return JsonResponse({'username': username},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        else:
            return JsonResponse({'error': '错误的用户名或密码'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )

    def is_login(request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        else:
            return JsonResponse({'message': '已登录',
                                 'username': request.user.username
                                 },
                                status=status.HTTP_200_OK,
                                safe=False
                                )

    def sign_out(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        try:
            logout(request, request.user)
            return JsonResponse({'message': '登出成功'},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def all_post(request):
        lst = Post.objects.all()
        return JsonResponse(serializers.serialize('json', lst),
                            status=status.HTTP_200_OK,
                            safe=False
                            )

    def page(request):
        page_size = request.GET.get('page_size')
        index = request.GET.get('index')
        if not page_size or not index:
            return JsonResponse({'error': '参数错误'},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )
        try:
            pages = Paginator(Post.objects().all(), page_size)
            ret = pages(index)
            return JsonResponse(serializers.serialize(pages.object_list),
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )

    def new_post(request):
        if request.user.is_authenticated:
            post = PostSerializer(request.GET)
            post.save()
            return JsonResponse({'message': '发布成功'},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        else:
            return JsonResponse({'error': '发布失败'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )

    def like(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        try:
            username = request.user.username
            pid = request.GET.get('pid')
            post = Post.objects.filter(id=pid)
            if not post:
                # 留言不存在
                return JsonResponse({'error': '留言不存在'},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False
                                    )
            attitude = Attitue.objects().filter(pid=id, username=username)
            if not attitude:
                # 此前用户对这条留言没有态度
                new_attitude = AttitudeSerializer(username=username,
                                                  pid=pid,
                                                  attitude=ATTITUTE.LIKE
                                                  )
                new_attitude.save()
            elif attitude.attitude == ATTITUTE.LIKE:
                # 此前为赞，取消赞
                attitude.delete()
            elif attitude.attitude == ATTITUTE.HATE:
                # 此前为踩，改为赞
                attitude.update(attitude=ATTITUTE.LIKE)
            return JsonResponse({'message': '完成'},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error', str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )

    def hate(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        try:
            username = request.user.username
            pid = request.GET.get('pid')
            post = Post.objects.filter(id=pid)
            if not post:
                # 留言不存在
                return JsonResponse({'error': '留言不存在'},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False
                                    )
            attitude = Attitue.objects().filter(pid=id, username=username)
            if not attitude:
                # 此前用户对这条留言没有态度
                new_attitude = AttitudeSerializer(username=username,
                                                  pid=pid,
                                                  attitude=ATTITUTE.HATE
                                                  )
                new_attitude.save()
            elif attitude.attitude == ATTITUTE.HATE:
                # 此前为踩，取消踩
                attitude.delete()
            elif attitude.attitude == ATTITUTE.LIKE:
                # 此前为赞，改为踩
                attitude.update(attitude=ATTITUTE.HATE)
            return JsonResponse({'message': '完成'},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error', str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )

