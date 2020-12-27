from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import pandas as pd
from .models import (
    Recipe,
    Tag,
    Favourites,
    Subscriptions,
    Purchases,
    Ingredient,
    Quantity
)
from .utils import (
    get_purchases,
    get_favorite,
    get_ingredients_create_recipe,
    get_tag_create_recipe
)
from .forms import RecipeForm

User = get_user_model()

PAGE_COUNT = 9


class Index(View):

    def get(self, request):
        tag_list = request.GET.getlist('tag')
        if tag_list != []:
            recipe_list = Recipe.objects.filter(
                tag__tag__in=tag_list
                ).order_by('-pub_date').all()
        else:
            recipe_list = Recipe.objects.order_by('-pub_date').all()
        paginator = Paginator(recipe_list, PAGE_COUNT)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        if request.user.is_authenticated:
            favorite = Favourites.objects.filter(user=request.user).values_list('recipe_id')
            favorite_list = []
            for i in favorite:
                favorite_list.append(i[0])
            return render(request, 'index.html', {
                'page': page,
                'paginator': paginator,
                'purchases_list': get_purchases(request),
                'favorite_list': get_favorite(request),
                'tag_list': tag_list
                })
        else:
            return render(request, 'index.html', {
                'page': page,
                'paginator': paginator,
                'tag_list': tag_list
            })


def author_ricipe(request, username):
    if request.method == 'GET':
        tag_list = request.GET.getlist('tag')
        profile = get_object_or_404(User, username=username)
        if tag_list != []:
            recipe_list = Recipe.objects.filter(
                author__username=profile
                ).filter(tag__tag__in=tag_list).order_by('-pub_date')
        else:
            recipe_list = Recipe.objects.filter(
                author__username=profile
                ).order_by('-pub_date')
        paginator = Paginator(recipe_list, PAGE_COUNT)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        if request.user.is_authenticated:
            subscribers = Subscriptions.objects.filter(
                user__username=request.user,
                author__username=profile.username
                )
            return render(request, 'author_recipe.html', {
                'page': page,
                'paginator': paginator,
                'profile': profile,
                'subscribers': subscribers,
                'favorite_list': get_favorite(request),
                'purchases_list': get_purchases(request),
                'tag_list': tag_list
                })
        else:
            return render(request, 'author_recipe.html', {
                'page': page,
                'paginator': paginator,
                'profile': profile,
                'tag_list': tag_list
            })


def single(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id).exists()
    if not recipe:
        return render(
            request, 
            "misc/404.html", 
            {"path": request.path}, 
            status=404
        )
    recipe = Recipe.objects.get(pk=recipe_id)
    if request.user.is_authenticated:
        favorite = Favourites.objects.filter(
            user=request.user,
            recipe_id=recipe_id
            )
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        subscribers = Subscriptions.objects.filter(
            user__username=request.user,
            author=recipe.author
            )
        return render(request, 'single_page.html', {
            'recipe': recipe,
            'favorite': favorite,
            'subscribers': subscribers,
            'purchases_list': get_purchases(request)
            })
    else:
        return render(request, 'single_page.html', {'recipe': recipe})


@login_required
def favourites(request):
    if request.method == 'GET':
        tag_list = request.GET.getlist('tag')
        profile = get_object_or_404(User, username=request.user)
        if tag_list != []:
            recipe_list = Favourites.objects.filter(
                user__username=profile
                ).filter(recipe__tag__tag__in=tag_list)
        else:
            recipe_list = Favourites.objects.filter(
                user__username=request.user
                )
        paginator = Paginator(recipe_list, PAGE_COUNT)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'favorite.html', {
            'page': page,
            'paginator': paginator,
            'purchases_list': get_purchases(request),
            'tag_list': tag_list
            })


@login_required
def subscriptions_list(request):
    if request.method == 'GET':
        subscribers = Subscriptions.objects.filter(
            user__username=request.user
            )
        authers = []
        for author in subscribers:
            authers.append(author.author)
        recipe_list = []
        for author in authers:
            recipe = Recipe.objects.filter(
                author=author
                ).order_by('-pub_date')[:3]
            recipe_countt = Recipe.objects.filter(
                author=author
                ).count() - 3
            recipe_list.append({
                'author': author,
                'recipe': recipe,
                'recipe_countt': recipe_countt
                })
        paginator = Paginator(recipe_list, PAGE_COUNT)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'my_follow.html', {
            'page': page,
            'paginator': paginator
            })


@login_required
def purchases(request):
    if request.method == 'GET':
        recipe_list = Purchases.objects.filter(
            user__username=request.user
            )
        return render(request, 'shop_list.html', {
            'recipe_list': recipe_list,
            })


@login_required
def purchases_file(request):
    if request.method == 'GET':
        recipe_list = Purchases.objects.filter(user__username=request.user)
        recipes = []
        for recipe in recipe_list:
            recipes.append(recipe.recipe.pk)
        recipe = Recipe.objects.filter(pk__in=recipes)
        ingredients = []
        for i in recipe:
            for j in i.quantity.all():
                ingredients.append([
                    j.ingr.title,
                    j.quantity,
                    j.ingr.dimension
                    ])
        ingredients_final = []
        for i in ingredients:
            if ingredients_final != []:
                for j in range(len(ingredients_final)):
                    if i[0] == ingredients_final[j][0]:
                        ingredients_final[j] = [
                            i[0],
                            i[1]+ingredients_final[j][1],
                            i[2]
                            ]
                        break
                    elif j == len(ingredients_final)-1:
                        ingredients_final.append(i)
            else:
                ingredients_final.append(i)
        final =  pd.DataFrame(pd.Series(ingredients_final, name = 'column1'))
        final_2 = final.to_string(header=False, index=True)
        response = HttpResponse(
            final_2,
            content_type='application/.txt'
            )
        response['Content-Disposition'] = \
            'attachment; filename="purchases.txt"'
        return response


@login_required
def create_recipe(request):
    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients_create_recipe(request)
        if ingredients == []:
            #проверка на наличие ингридиентов
            form.add_error(None, 'Не добавлены ингридиенты')
        tags = get_tag_create_recipe(request)
        if tags == []:
            #проверка на наличие тегов
            form.add_error(None, 'Не добавлены теги')
        for i in ingredients:
            #проверяем есть ли ингридиенты в базе
            ingredient = Ingredient.objects.filter(title=i['title']).exists()
            if not ingredient:
                form.add_error(None, 'Таких ингридиентов не существует')
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            for i in ingredients:
                #добавляем ингридиенты к рецепту
                ingredient = get_object_or_404(Ingredient, title=i['title'])
                quantity_obj = Quantity.objects.get_or_create(ingr=ingredient, quantity=i['value'])[0]
                new.quantity.add(quantity_obj)
            for i in tags:
                #добавляем теги к рецепту
                tag = get_object_or_404(Tag, tag=i)
                new.tag.add(tag)
            form.save_m2m()
            return redirect('index')
    return render(request, 'form_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=id)
    ingredientes = recipe.quantity.all()
    form = RecipeForm()
    tag = recipe.tag.all() #получаем теги рецепта
    tags = []
    for i in tag:
        tags.append(i.tag)
    if request.user != profile:
        #user должен быть автором рецепта
        return redirect('single', id)
    if request.method == 'POST':
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
            )
        ingredients = get_ingredients_create_recipe(request)
        #получаем список ингридиентов из POST запроса
        if ingredients == []:
            #проверка на наличие ингридиентов
            form.add_error(None, 'Не добавлены ингридиенты')
        for i in ingredients:
            #проверяем есть ли ингридиенты в базе
            ingredient = Ingredient.objects.filter(title=i['title']).exists()
            if not ingredient:
                form.add_error(None, 'Таких ингридиентов не существует')
        tags = get_tag_create_recipe(request)
        if tags == []:
            #проверяем на наличии тегов
            form.add_error(None, 'Не добавлены теги')
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            new.quantity.clear()#убираем прежний список ингридиентов
            for i in ingredients:
                #проверяем в БД есть ли данный объект в моделе Quantity
                #если есть он возвращается, если нет он создается
                ingredient = get_object_or_404(Ingredient, title=i['title'])
                quantity_obj = Quantity.objects.get_or_create(ingr=ingredient, quantity=i['value'])[0]
                new.quantity.add(quantity_obj)
            new.tag.clear()#убирает те теги что былии ранее
            for i in tags:
                #добавляем теги
                tag = get_object_or_404(Tag, tag=i)
                new.tag.add(tag)
            form.save_m2m()
            return redirect('single', recipe.pk)

    return render(request, 'form_change_recipe.html', {
        'recipe': recipe,
        'ingredientes': ingredientes,
        'tags': tags,
        'form': form
        })


def delete_recipe(request, username, id):
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        Recipe.objects.filter(
            author__username=username,
            pk=id
        ).delete()
    return redirect('index')


def purchases_del_not_js(request, id):
    Purchases.objects.get(recipe_id=id).delete()
    recipe_list = Purchases.objects.filter(user__username=request.user)
    return render(request, 'shop_list.html', {
        'recipe_list': recipe_list,
        })

def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )
