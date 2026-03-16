from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .pagination import CustomPageNumberPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 处理筛选参数
        category = self.request.query_params.get('category', None)
        status = self.request.query_params.get('status', None)
        search = self.request.query_params.get('search', None)
        publisher = self.request.query_params.get('publisher', None)
        
        if category:
            queryset = queryset.filter(category_id=category)
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        if publisher:
            queryset = queryset.filter(publisher=publisher)
        
        return queryset
    
    def perform_create(self, serializer):
        # 设置发布者为当前登录用户的用户名
        if self.request.user.is_authenticated:
            # 检查用户类型，处理前台用户和后台用户
            if hasattr(self.request.user, 'username'):
                serializer.save(publisher=self.request.user.username)
            else:
                serializer.save()
        else:
            # 未登录用户使用默认发布者名称
            serializer.save(publisher='匿名用户')