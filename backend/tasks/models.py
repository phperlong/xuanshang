from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # 从name生成slug
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('open', '进行中'),
        ('completed', '已完成'),
    ]
    
    CATEGORY_CHOICES = [
        ('design', '设计'),
        ('development', '开发'),
        ('writing', '写作'),
        ('translation', '翻译'),
        ('reward', '悬赏'),
        ('game', '游戏'),
        ('trade', '交易'),
        ('charity', '公益'),
        ('other', '其他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='任务标题')
    category_id = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='任务分类')
    reward = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='悬赏金额')
    deadline = models.DateField(verbose_name='截止日期')
    description = models.TextField(verbose_name='任务描述')
    contact = models.CharField(max_length=200, verbose_name='联系方式')
    publisher = models.CharField(max_length=100, default='匿名用户', verbose_name='发布者')
    assignee = models.CharField(max_length=100, null=True, blank=True, verbose_name='接受者')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title