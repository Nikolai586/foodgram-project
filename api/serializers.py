from rest_framework import serializers
from recipe.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')
