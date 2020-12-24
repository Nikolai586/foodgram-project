from django.core.management.base import BaseCommand
from recipe.models import Tag

TAGS = ['breakfast', 'lunch', 'dinner']

class Command(BaseCommand):
    help = 'Создание тегов'

    def handle(self, *args, **options):
        for i in TAGS:
            Tag.objects.create(tag=i)
        return print('Теги созданы')
