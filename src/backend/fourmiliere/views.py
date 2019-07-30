from django.http import JsonResponse
from rest_framework import viewsets
from .models import User, Post, Attitude
from .models import ATTITUTE
from .serializers import UserSerializer, PostSerializer, AttitudeSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.paginator import Paginator


class MyError(Exception):
    pass


class AttitudeView(viewsets.ModelViewSet):
    queryset = Attitude.objects.all()
    serializer_class = AttitudeSerializer


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
            logout(request)
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

    @staticmethod
    def add_myattitude(request, lst):
        ret = []
        if request.user.is_authenticated:
            username = request.user.username
            for i in lst:
                attitude = Attitude.objects.filter(username=username,
                                                   pid=i.pid)
                i['attitude'] = attitude.attitude
                ret.append(i)
        else:
            for i in lst:
                i['attitude'] = ATTITUTE.UNDE
                ret.append(i)
        return ret

    def all_post(request):
        lst = Post.objects.all()
        # lst = PostView.add_myattitude(request, lst)
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
            pages = Paginator(Post.objects.all(), page_size)
            pages = pages.get_page(index)
            ret = pages(index).object_list
            # ret = PostView.add_myattitude(request, ret)
            return JsonResponse(serializers.serialize(ret),
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )

    def new_post(request):
        postbody = request.GET.copy()
        postbody._mutable = True
        postbody['username'] = request.user.username
        postbody['like'] = 0
        postbody['hate'] = 0
        postbody['create_time'] = int(postbody['create_time'])
        post = PostSerializer(data=postbody)
        if request.user.is_authenticated and post.is_valid():
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
        # return JsonResponse({str(type(Attitude)): str(type(Post))})
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        try:
            username = request.user.username
            pid = request.GET.get('pid')
            pid = int(pid)
            post = Post.objects.get(id=pid)
            if not post:
                # 留言不存在
                return JsonResponse({'error': '留言不存在'},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False
                                    )
            attitude = Attitude.objects.filter(pid=pid)
            if len(attitude) > 0:
                attitude = attitude.get(username=username)
            if not attitude:
                # 此前用户对这条留言没有态度
                pack = {
                    'username': username,
                    'pid': pid,
                    'attitude': ATTITUTE.LIKE.value
                }
                new_attitude = AttitudeSerializer(data=pack)
                if new_attitude.is_valid():
                    new_attitude.save()
                    post.like = post.like + 1
                    post.save()
                else:
                    raise MyError('invalid data')
            elif attitude.attitude == ATTITUTE.LIKE.value:
                # 此前为赞，取消赞
                attitude.delete()
                post.like = post.like - 1
                post.save()
            elif attitude.attitude == ATTITUTE.HATE.value:
                # 此前为踩，改为赞
                attitude.attitude = ATTITUTE.LIKE.value
                attitude.save()
                post.like = post.like + 1
                post.hate = post.hate - 1
                post.save()
            return JsonResponse({'message': '完成',
                                 'like': post.like,
                                 'hate': post.hate},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error', ''},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )

    def hate(request):
        # return JsonResponse({str(type(Attitude)): str(type(Post))})
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'},
                                status=status.HTTP_401_UNAUTHORIZED,
                                safe=False
                                )
        try:
            username = request.user.username
            pid = request.GET.get('pid')
            pid = int(pid)
            post = Post.objects.get(id=pid)
            if not post:
                # 留言不存在
                return JsonResponse({'error': '留言不存在'},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False
                                    )
            attitude = Attitude.objects.filter(pid=pid)
            if len(attitude) > 0:
                attitude = attitude.get(username=username)
            if not attitude:
                # 此前用户对这条留言没有态度
                pack = {
                    'username': username,
                    'pid': pid,
                    'attitude': ATTITUTE.HATE.value
                }
                new_attitude = AttitudeSerializer(data=pack)
                if new_attitude.is_valid():
                    new_attitude.save()
                    post.hate = post.hate + 1
                    post.save()
                else:
                    raise MyError('invalid data')
            elif attitude.attitude == ATTITUTE.HATE.value:
                # 此前为踩，取消踩
                attitude.delete()
                post.hate = post.hate - 1
                post.save()
            elif attitude.attitude == ATTITUTE.LIKE.value:
                # 此前为赞，改为踩
                attitude.attitude = ATTITUTE.HATE.value
                attitude.save()
                post.like = post.like - 1
                post.hate = post.hate + 1
                post.save()
            return JsonResponse({'message': '完成',
                                 'hate': post.hate,
                                 'like': post.like},
                                status=status.HTTP_200_OK,
                                safe=False
                                )
        except Exception as e:
            return JsonResponse({'error', ''},
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False
                                )
