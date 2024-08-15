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

class PredefinedResponse(models.Model):
  """
  Model to store predefined questions and their corresponding responses.
  """
  question = models.CharField(max_length=255, unique=True)
  response = models.TextField()

  def __str__(self):
    return self.question

class Chat(models.Model):
  """
  Model to represent a chat session between a user and the assistant.
  """
  # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Chat {self.id} started at {self.created_at}"

class Message(models.Model):
  """
  Model to store individual messages within a chat.
  """
  SENDER_CHOICES = [
    ('user', 'User'),
    ('assistant', 'Assistant'),
  ]

  chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
  sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.sender}: {self.content[:30]}..."