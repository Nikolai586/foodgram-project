from django.core.management.base import BaseCommand
import csv
from app.models import Ingredient


class Command(BaseCommand):
    help = 'Заполнение БД ингридиентами'

    def handle(self, *args, **options):
        with open('ingredients.csv', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for i in file_reader:
                Ingredient.objects.create(title=i[0], dimension=i[1])
        return print('Ингредиенты созданы')
