from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from frontend_users.models import FrontendUser

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response(
                {'error': '请提供用户名、邮箱和密码'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if FrontendUser.objects.filter(username=username).exists():
            return Response(
                {'error': '用户名已存在'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if FrontendUser.objects.filter(email=email).exists():
            return Response(
                {'error': '邮箱已被注册'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = FrontendUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': '请提供用户名和密码'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'error': '用户名或密码错误'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_200_OK
        )

class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_200_OK
        )