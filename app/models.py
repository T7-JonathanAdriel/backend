from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
  def create_user(self, username, name, password=None):
    if not username:
      raise ValueError("Username is required.")
    if not name:
      raise ValueError("Name is required.")
    if not password:
      raise ValueError("Password is required.")

    user = self.model(username=username, name=name)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, name, password=None):
    user = self.create_user(username, name, password)
    user.is_superuser = True
    user.save(using=self._db)
    return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=255)
  password = models.CharField(max_length=128)
  
  groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
  user_permissions = models.ManyToManyField(
    Permission, related_name="custom_users", blank=True
  )

  objects = CustomUserManager()

  USERNAME_FIELD = "username"
  REQUIRED_FIELDS = ["name", "password"]

  def __str__(self):
    return self.username
