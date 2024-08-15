from django.core.management.base import BaseCommand
from ...models import PredefinedResponse

class Command(BaseCommand):
  help = 'Seed predefined responses into the database'

  def handle(self, *args, **kwargs):
    responses = [
      {"question": "What are common household items?", "response": "Common household items include:\n1. A vacuum cleaner\n2. A toaster\n3. A microwave\n4. A coffee maker\n5. A blender"},
      {"question": "What are everyday essentials to carry?", "response": "Everyday essentials to carry might be:\n1. A wallet\n2. A phone\n3. Keys\n4. A reusable water bottle\n5. Personal identification"},
      {"question": "What are popular hobbies?", "response": "Popular hobbies include:\n1. Reading\n2. Gardening\n3. Cooking\n4. Painting\n5. Playing a musical instrument"},
      {"question": "What are common school items?", "response": "Common school items include:\n1. A backpack\n2. Notebooks\n3. Pens and pencils\n4. A calculator\n5. Textbooks"},
      {"question": "What are typical weekend activities?", "response": "Typical weekend activities include:\n1. Going for a hike\n2. Watching movies\n3. Visiting friends or family\n4. Shopping\n5. Relaxing at home"},
      {"question": "hi", "response": "Hello! How can I help you today?"},
      {"question": "test", "response": "Test received! How can I help you?"},
      {"question": "", "response": "It looks like you've sent an empty message."},
      {"question": "hahahahahhahahahha", "response": "It looks like you're in a good mood!"},
    ]

    for item in responses:
      PredefinedResponse.objects.get_or_create(question=item['question'], response=item['response'])
      self.stdout.write(self.style.SUCCESS(f"Created response for question: {item['question']}"))
