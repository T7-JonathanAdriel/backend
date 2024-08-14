from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.hashers import check_password

@csrf_exempt
def register(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    form = CustomUserCreationForm(data)

    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(data.get('password1'))
      user.save()
      
      return JsonResponse({'message': 'User registered successfully'}, status=201)
    
    return JsonResponse({'error': form.errors.as_json()}, status=400)

@csrf_exempt
def user_login(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
      return JsonResponse({'error': 'Username and password are required'}, status=400)

    try:
      user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
      return JsonResponse({'error': 'Invalid credentials'}, status=400)

    if check_password(password, user.password):
      # login(request, user)
      return JsonResponse({'message': 'User logged in successfully'}, status=200)
  
  return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def user_logout(request):
  if request.method == 'POST':
    # logout(request)
    return JsonResponse({'message': 'User logged out successfully'}, status=200)
