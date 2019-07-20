from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
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
                user = User.objects.create_user(username=username, password=password)
                return JsonResponse({'username': user.username}, status=status.HTTP_200_OK, safe=False)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST, safe=False)
        return JsonResponse({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
    def sign_in(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(request=request, nickname=username, password=password)
        if not user:
            return JsonResponse({'username': username}, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED, safe=False)
