from django import forms
from .models import Ingredient, Recipe, Quantity


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class QuantityForm(forms.ModelForm):

    class Meta:
        model = Quantity
        fields = ['quantity', 'ingr']


class TagFilter(forms.Form):
    tag = forms.CharField(max_length=50)


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'image',
            'cooking_time',
        ]
