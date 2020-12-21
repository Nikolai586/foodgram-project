from django.core.management.base import BaseCommand
from recipe.models import Tag


class Command(BaseCommand):
    help = 'Создание тегов'

    def handle(self, *args, **options):
        tags = ['breakfast', 'lunch', 'dinner']
        for i in tags:
            Tag.objects.create(tag=i)
        return print('Теги созданы')
