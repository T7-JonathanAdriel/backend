from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from ..models import Chat, Message, PredefinedResponse
import json

def get_chat_title(request):
  chats = Chat.objects.all().order_by('-updated_at')
  chat_data = []

  for chat in chats:
    first_message = Message.objects.filter(chat=chat).first()
    message_content = first_message.content if first_message else ""
    title = (
      message_content[:30] + ("..." if len(message_content) > 30 else "")
    ) if message_content else "Untitled chat"
    
    chat_data.append({
      "id": chat.id,
      "title": title
    })

  response_data = {
    "chats": chat_data
  }

  return JsonResponse(response_data, status=200)
  
def get_chat_by_id(request, id):
  try:
    chat = Chat.objects.get(pk=id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    
    messages_data = [
      {
        "id": message.id,
        "sender": message.sender,
        "content": message.content,
        "timestamp": message.timestamp.isoformat()
      }
      for message in messages
    ]
    
    response_data = {
      "messages": messages_data
    }
    return JsonResponse(response_data, status=200)
  except Chat.DoesNotExist:
    return JsonResponse({"error": f"Chat with id {id} is not found"}, status=404)
  
@csrf_exempt
def create_chat(request):
  if request.method == 'POST':
    try:
      chat = Chat.objects.create()
      response_data = {
        'id': chat.id,
        'created_at': chat.created_at.isoformat(),
        'updated_at': chat.updated_at.isoformat(),
      }
      
      return JsonResponse(response_data, status=201)
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
def create_message(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    try:
      chat = Chat.objects.get(pk=data.get('chatId'))
      content = data.get('content').strip()
      
      message = Message.objects.create(
        chat=chat,
        sender='user',
        content=content
      )

      try:
        predefined_response = PredefinedResponse.objects.get(question__icontains=content)
        assistant_content = predefined_response.response
      except PredefinedResponse.DoesNotExist:
        top_questions = PredefinedResponse.objects.values_list('question', flat=True).order_by('id')[:3]
        assistant_content = (
          "I don't know the answer to your question. Please try one of the following:"
          f"\n{[f"- {q}" for q in top_questions]}"
        )
      
      assistant_message = Message.objects.create(
        chat=chat,
        sender='assistant',
        content=assistant_content
      )

      chat.updated_at = assistant_message.timestamp.isoformat()
      chat.save()
      
      response_data = {
        "id": message.id,
        "sender": message.sender,
        "content": message.content,
        "timestamp": message.timestamp.isoformat()
      }
      return JsonResponse(response_data, status=201)
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
@csrf_exempt
def create_message(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      chat = Chat.objects.get(pk=data.get('chatId'))
      content = data.get('content').strip()

      user_message = Message.objects.create(
        chat=chat,
        sender='user',
        content=content
      )

      assistant_content = get_assistant_response(content)

      assistant_message = Message.objects.create(
        chat=chat,
        sender='assistant',
        content=assistant_content
      )

      chat.updated_at = assistant_message.timestamp
      chat.save()

      response_data = {
        "messages": [
          format_message_response(user_message),
          format_message_response(assistant_message)
        ]
      }

      return JsonResponse(response_data, status=201)
    except (json.JSONDecodeError, Chat.DoesNotExist):
      return JsonResponse({'error': 'Invalid request'}, status=400)

def get_assistant_response(content):
  try:
    predefined_response = PredefinedResponse.objects.filter(
      question__icontains=content
    ).first()
    
    if predefined_response:
      return predefined_response.response
    else:
      raise PredefinedResponse.DoesNotExist
  except PredefinedResponse.DoesNotExist:
    top_questions = PredefinedResponse.objects.values_list('question', flat=True).order_by('id')[:3]
    return (
      "I don't know the answer to your question. Please try one of the following:\n" +
      ''.join([f'- {q}\n' for q in top_questions])
    )

def format_message_response(message):
  return {
    "id": message.id,
    "sender": message.sender,
    "content": message.content,
    "timestamp": message.timestamp.isoformat()
  }
