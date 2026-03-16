from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category_id')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'category', 'reward', 'deadline', 'description', 'contact', 'publisher', 'assignee', 'status', 'created_at']
    
    def create(self, validated_data):
        # 处理category字段
        if 'category_id' in validated_data:
            pass
        elif 'category' in validated_data:
            validated_data['category_id'] = validated_data.pop('category')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # 处理category字段
        if 'category' in validated_data:
            validated_data['category_id'] = validated_data.pop('category')
        return super().update(instance, validated_data)