from .models import (
    Purchases,
    Favourites
)


def get_purchases(request):
    purchases = Purchases.objects.filter(user__username=request.user).values_list('recipe_id')
    purchases_list = []
    for i in purchases:
        purchases_list.append(i[0])
    return purchases_list


def get_favorite(request):
    favorite = Favourites.objects.filter(user=request.user).values_list('recipe_id')
    favorite_list = []
    for i in favorite:
        favorite_list.append(i[0])
    return favorite_list


def get_ingredients_create_recipe(request):
    ingredient_list = []
    for i, j in request.POST.items():
        if 'nameIngredient' in i:
            temp = i.split('_')
            ingredient_list.append({
                'title': j,
                'value': int(request.POST[f'valueIngredient_{temp[1]}'])})
    return ingredient_list


def get_tag_create_recipe(request):
    tags_list = []
    for i, j in request.POST.items():
        if j == 'on':
            tags_list.append(i)
    return tags_list