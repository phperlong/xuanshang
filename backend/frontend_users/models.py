from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class FrontendUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('用户名不能为空')
        if not email:
            raise ValueError('邮箱不能为空')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class FrontendUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    email = models.EmailField(max_length=255, unique=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    objects = FrontendUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = '前台用户'
        verbose_name_plural = '前台用户'
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin