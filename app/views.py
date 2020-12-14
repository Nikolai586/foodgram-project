from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import (
    Recipe,
    Tag,
    Favourites,
    Subscriptions,
    Purchases,
    Ingredient,
    Quantity
)
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .filters import tag_filter, tag_filter_author, tag_filter_favourites
import json
from django.http import JsonResponse, HttpResponse

User = get_user_model()


class Index(View):

    def get(self, request):
        tag1 = request.GET.get('tag1')
        tag2 = request.GET.get('tag2')
        tag3 = request.GET.get('tag3')
        if tag1 is not None or tag2 is not None or tag3 is not None:
            recipe_list = tag_filter(tag1, tag2, tag3)
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            if request.user.is_authenticated:
                purchases = Purchases.objects.filter(user__username=request.user)
                favorite = Favourites.objects.filter(user=request.user)
                recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
                purchases_list = []
                favorite_list = []
                for i in favorite:
                    favorite_list.append(i.recipe.title)
                for i in purchases:
                    purchases_list.append(i.recipe.title)
                return render(request, 'index.html', {
                    'page': page,
                    'paginator': paginator,
                    'recipe_bay_count': recipe_bay_count,
                    'purchases_list': purchases_list,
                    'favorite_list': favorite_list
                    })
            else:
                return render(request, 'index.html', {'page': page, 'paginator': paginator})
        else:
            recipe_list = Recipe.objects.order_by('-pub_date').all()
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            if request.user.is_authenticated:
                purchases = Purchases.objects.filter(user__username=request.user)
                favorite = Favourites.objects.filter(user=request.user)
                recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
                purchases_list = []
                favorite_list = []
                for i in favorite:
                    favorite_list.append(i.recipe.title)
                for i in purchases:
                    purchases_list.append(i.recipe.title)
                return render(request, 'index.html', {
                    'page': page,
                    'paginator': paginator,
                    'recipe_bay_count': recipe_bay_count,
                    'purchases_list': purchases_list,
                    'favorite_list': favorite_list
                    })
            else:
                return render(request, 'index.html', {'page': page, 'paginator': paginator})


def author_ricipe(request, username):
    if request.method == 'GET':
        tag1 = request.GET.get('tag1')
        tag2 = request.GET.get('tag2')
        tag3 = request.GET.get('tag3')
        profile = get_object_or_404(User, username=username)
        if tag1 is not None or tag2 is not None or tag3 is not None:
            recipe_list = tag_filter_author(profile, tag1, tag2, tag3)
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            if request.user.is_authenticated:
                purchases = Purchases.objects.filter(user__username=request.user)
                subscribers = Subscriptions.objects.filter(user__username=request.user, author__username=profile.username)
                recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
                favorite = Favourites.objects.filter(user=request.user)
                favorite_list = []
                purchases_list = []
                for i in purchases:
                    purchases_list.append(i.recipe.title)
                for i in favorite:
                    favorite_list.append(i.recipe.title)
                return render(request, 'authorRecipe.html', {
                    'page': page, 'paginator': paginator,
                    'profile': profile,
                    'subscribers': subscribers,
                    'favorite_list': favorite_list,
                    'recipe_bay_count': recipe_bay_count,
                    'purchases_list': purchases_list
                    })
            else:
                return render(request, 'authorRecipe.html', {'page': page, 'paginator': paginator, 'profile': profile})
        else:
            recipe_list = Recipe.objects.filter(author__username=profile)
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            if request.user.is_authenticated:
                purchases = Purchases.objects.filter(user__username=request.user)
                subscribers = Subscriptions.objects.filter(user__username=request.user, author__username=profile.username)
                recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
                favorite = Favourites.objects.filter(user=request.user)
                favorite_list = []
                purchases_list = []
                for i in purchases:
                    purchases_list.append(i.recipe.title)
                for i in favorite:
                    favorite_list.append(i.recipe.title)
                return render(request, 'authorRecipe.html', {
                    'page': page,
                    'paginator': paginator,
                    'profile': profile,
                    'subscribers': subscribers,
                    'favorite_list': favorite_list,
                    'recipe_bay_count': recipe_bay_count,
                    'purchases_list': purchases_list
                    })
            else:
                return render(request, 'authorRecipe.html', {'page': page, 'paginator': paginator, 'profile': profile})


def single(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(user__username=request.user)
        favorite = Favourites.objects.filter(user=request.user, recipe_id=recipe_id)
        recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        subscribers = Subscriptions.objects.filter(user__username=request.user, author=recipe.author)
        purchases_list = []
        for i in purchases:
            purchases_list.append(i.recipe.title)
        return render(request, 'singlePage.html', {
            'recipe': recipe,
            'favorite': favorite,
            'subscribers': subscribers,
            'recipe_bay_count': recipe_bay_count,
            'purchases_list': purchases_list
            })
    else:
        return render(request, 'singlePage.html', {'recipe': recipe})

@login_required
def favourites(request):
    if request.method == 'GET':
        tag1 = request.GET.get('tag1')
        tag2 = request.GET.get('tag2')
        tag3 = request.GET.get('tag3')
        profile = get_object_or_404(User, username=request.user)
        if tag1 is not None or tag2 is not None or tag3 is not None:
            recipe_list = tag_filter_favourites(profile, tag1, tag2, tag3)
            recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
            purchases = Purchases.objects.filter(user__username=request.user)
            purchases_list = []
            for i in purchases:
                purchases_list.append(i.recipe.title)
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
        else:
            recipe_list = Favourites.objects.filter(user__username=request.user)
            recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
            purchases = Purchases.objects.filter(user__username=request.user)
            purchases_list = []
            for i in purchases:
                purchases_list.append(i.recipe.title)
            paginator = Paginator(recipe_list, 9)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
        return render(request, 'favorite.html', {
            'page': page,
            'paginator': paginator,
            'recipe_bay_count': recipe_bay_count,
            'purchases_list': purchases_list
            })

@login_required
def subscriptions_list(request):
    if request.method == 'GET':
        subscribers = Subscriptions.objects.filter(user__username=request.user)
        recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
        authers = []
        for author in subscribers:
            authers.append(author.author)
        recipe_list = []
        for author in authers:
            recipe = Recipe.objects.filter(author=author).order_by('-pub_date')[:3]
            recipe_count = Recipe.objects.filter(author=author).count() - 3
            recipe_list.append({'author': author, 'recipe': recipe, 'recipe_count': recipe_count})
        paginator = Paginator(recipe_list, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'myFollow.html', {
            'page': page,
            'paginator': paginator,
            'recipe_bay_count': recipe_bay_count
            })

@login_required
def purchases(request):
    if request.method == 'GET':
        recipe_list = Purchases.objects.filter(user__username=request.user)
        recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
        return render(request, 'shopList.html', {
            'recipe_list': recipe_list,
            'recipe_bay_count': recipe_bay_count
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
                ingredients.append([j.ingr.title, j.quantity, j.ingr.dimension])
        ingredients_final = []
        for i in ingredients:
            if ingredients_final != []:
                for j in range(len(ingredients_final)):
                    if i[0] == ingredients_final[j][0]:
                        ingredients_final[j] = [i[0], i[1]+ingredients_final[j][1], i[2]]
                        break
                    elif j == len(ingredients_final)-1:
                        ingredients_final.append(i)
            else:
                ingredients_final.append(i)
        response = HttpResponse(ingredients_final, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="purchases.txt"' # было расширение .xlsx
        return response


from django.core.files.storage import FileSystemStorage
from django.conf import settings

@login_required
def create_recipe(request):
    if request.method == 'POST':
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        request_dict = {}
        for i, j in request.POST.items():
            request_dict[i] = j
        request_dict.pop('name')
        request_dict.pop('cooking_time')
        request_dict.pop('description')
        request_dict.pop('csrfmiddlewaretoken')
        tags_list = []
        for i, j in request_dict.items():
            if j == 'on':
                tags_list.append(i)
        for i in tags_list:
            request_dict.pop(i)
        temporary_list = []
        request_list = []
        for i in request_dict.values():
            temporary_list.append(i)
            if len(temporary_list) == 3:
                request_list.append(temporary_list)
                temporary_list = []
        if request_list == [] or request.POST['description'] == '' or tags_list == []:
            return render(request, 'error.html')
        recipe = Recipe.objects.create(
            author=request.user,
            title=request.POST['name'],
            description=request.POST['description'],
            cooking_time=request.POST['cooking_time'],
            image=filename
            )
        for i in tags_list:
            tag = get_object_or_404(Tag, tag=i)
            recipe.tag.add(tag)
        for i in request_list:
            ingr = get_object_or_404(Ingredient, title=i[0])
            if Quantity.objects.filter(ingr=ingr, quantity=int(i[1])).exists():
                recipe.quantity.add(Quantity.objects.get(ingr=ingr, quantity=int(i[1])))
            else:
                quantity = Quantity.objects.create(ingr=ingr, quantity=int(i[1]))
                recipe.quantity.add(quantity)
        return redirect('single', recipe.pk)
    recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()        
    return render(request, 'formRecipe.html', {'recipe_bay_count': recipe_bay_count})

@login_required
def recipe_edit(request, username, id):
    recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        if request.method == 'POST':
            request_dict = {}
            for i, j in request.POST.items():
                request_dict[i] = j
            tags_list = []
            for i, j in request_dict.items():
                if j == 'on':
                    tags_list.append(i)
            for i in tags_list:
                request_dict.pop(i)
            request_dict.pop('name')
            request_dict.pop('cooking_time')
            request_dict.pop('description')
            request_dict.pop('csrfmiddlewaretoken')
            temporary_list = []
            request_list = []
            for i in request_dict.values():
                temporary_list.append(i)
                if len(temporary_list) == 3:
                    request_list.append(temporary_list)
                    temporary_list = []
            if request_list == [] or request.POST['description'] == '':
                return render(request, 'error.html')              
            if request.FILES:
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                recipe = Recipe.objects.filter(pk=id, author__username=username).update(
                    author=request.user,
                    title=request.POST['name'],
                    description=request.POST['description'],
                    cooking_time=request.POST['cooking_time'],
                    image=filename
                )
            else:
                recipe = Recipe.objects.filter(pk=id, author__username=username).update(
                    author=request.user,
                    title=request.POST['name'],
                    description=request.POST['description'],
                    cooking_time=request.POST['cooking_time'],
                )
                request_dict.pop('file')
            recipe = get_object_or_404(Recipe, pk=id, author__username=username)
            recipe.tag.clear()
            recipe.quantity.clear()
            for i in tags_list:
                tag = get_object_or_404(Tag, tag=i)
                recipe.tag.add(tag)                    
            for i in request_list:
                ingr = get_object_or_404(Ingredient, title=i[0])
                if Quantity.objects.filter(ingr=ingr, quantity=int(i[1])).exists():
                    recipe.quantity.add(Quantity.objects.get(ingr=ingr, quantity=int(i[1])))
                else:
                    quantity = Quantity.objects.create(ingr=ingr, quantity=int(i[1]))
                    recipe.quantity.add(quantity)
            return redirect('single', recipe.pk)
        else:
            if request.user == profile:
                recipe = get_object_or_404(Recipe, pk=id)
                ingredientes = recipe.quantity.all()
                tag = recipe.tag.all()
                tags = []
                for i in tag:
                    tags.append(i.tag)
                print(tags)
                return render(request, 'formChangeRecipe.html', {
                    'recipe_bay_count': recipe_bay_count,
                    'recipe': recipe,
                    'ingredientes': ingredientes,
                    'tags': tags
                    })
    else:
        recipe = get_object_or_404(Recipe, pk=id)
        return redirect('single', recipe.pk)

def delete_recipe(request, username, id):
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        Recipe.objects.filter(
            author__username=username,
            pk=id
        ).delete()
    return redirect('index')
    

########   Дальше идет код для JS   #########

def get_ingredients(request):
    text = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=text).values_list('title', 'dimension')
    ingredients_list = []
    if ingredients:
        for obj in ingredients:
            ingredients_list.append({'title': obj[0], 'dimension': obj[1]})
        return JsonResponse(ingredients_list, safe=False)
    else:
        return JsonResponse({'success': False})

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

def purchases_del_not_js(request, id):
    Purchases.objects.get(recipe_id=id).delete()
    recipe_list = Purchases.objects.filter(user__username=request.user)
    recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
    return render(request, 'shopList.html', {'recipe_list': recipe_list, 'recipe_bay_count': recipe_bay_count})

######### Залив БД ингридиентов #########
import csv
def base(request):
    with open('ingredients.csv', encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter = ",")
        for i in file_reader:
            Ingredient.objects.create(title=i[0], dimension=i[1])
    return redirect('index')

######## создание тегов ########
def create_tags(request):
    tags = ['breakfast', 'lunch', 'dinner']
    for i in tags:
        Tag.objects.create(tag=i)