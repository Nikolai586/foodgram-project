from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import (
    Ingredient,
    Favourites,
    Subscriptions,
    Purchases
)
from .serializers import RecipeSerializer


class GetIngredient(APIView):

    def get(self, request):
        text = request.GET.get('query')
        ingredients = Ingredient.objects.filter(title__contains=text)
        serializer = RecipeSerializer(ingredients, many=True)
        return Response(serializer.data)


@login_required
def favourites_add(request):
    if request.method == 'POST':
        id = int(json.loads(request.body).get('id'))
        created = Favourites.objects.get_or_create(
            user_id=request.user.id, recipe_id=id
        )
        if not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def favourites_del(request, id):
    if request.method == 'DELETE':
        delete = Favourites.objects.filter(
            user_id=request.user.id, recipe_id=id
        ).delete()
        if not delete:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def subscriptions_add(request):
    if request.method == 'POST':
        id = int(json.loads(request.body).get('id'))
        created = Subscriptions.objects.get_or_create(
            user_id=request.user.id, author_id=id
        )
        if not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def subscriptions_del(request, id):
    if request.method == 'DELETE':
        delete = Subscriptions.objects.filter(
            user_id=request.user.id, author_id=id
        ).delete()
        if not delete:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def subscriptions_del_name(request, username):
    if request.method == 'DELETE':
        delete = Subscriptions.objects.filter(
            user_id=request.user.id, author=username
        ).delete()
        if not delete:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def purchases_add(request):
    if request.method == 'POST':
        id = int(json.loads(request.body).get('id'))
        created = Purchases.objects.get_or_create(
                user_id=request.user.id, recipe_id=id
        )
        if not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def purchases_del(request, id):
    if request.method == 'DELETE':
        delete = Purchases.objects.filter(
            user_id=request.user.id, recipe_id=id
        ).delete()
        if not delete:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
