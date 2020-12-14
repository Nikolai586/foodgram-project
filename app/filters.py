from django.shortcuts import get_object_or_404
from .models import Recipe, Tag, Favourites
from django.db.models import Q


def tag_filter(tag1=None, tag2=None, tag3=None):
    tag_1 = None
    tag_2 = None
    tag_3 = None
    if tag1 is not None:
        tag_1 = get_object_or_404(Tag, tag=tag1)
    if tag2 is not None:
        tag_2 = get_object_or_404(Tag, tag=tag2)
    if tag3 is not None:
        tag_3 = get_object_or_404(Tag, tag=tag3)
    if tag_1 is not None or tag_2 is not None or tag_3 is not None:
        recipe_list = Recipe.objects.filter(Q(tag__tag=tag_1) | Q(tag__tag=tag_2) | Q(tag__tag=tag_3)).order_by('-pub_date')
    return recipe_list

def tag_filter_author(username, tag1=None, tag2=None, tag3=None):
    tag_1 = None
    tag_2 = None
    tag_3 = None
    if tag1 is not None:
        tag_1 = get_object_or_404(Tag, tag=tag1)
    if tag2 is not None:
        tag_2 = get_object_or_404(Tag, tag=tag2)
    if tag3 is not None:
        tag_3 = get_object_or_404(Tag, tag=tag3)
    if tag_1 is not None or tag_2 is not None or tag_3 is not None:
        recipe_list = Recipe.objects.filter(
            author__username=username
            ).filter(Q(tag__tag=tag_1) | Q(tag__tag=tag_2) | Q(tag__tag=tag_3)).order_by('-pub_date')
    return recipe_list

def tag_filter_favourites(username, tag1=None, tag2=None, tag3=None):
    tag_1 = None
    tag_2 = None
    tag_3 = None
    if tag1 is not None:
        tag_1 = get_object_or_404(Tag, tag=tag1)
    if tag2 is not None:
        tag_2 = get_object_or_404(Tag, tag=tag2)
    if tag3 is not None:
        tag_3 = get_object_or_404(Tag, tag=tag3)
    if tag_1 is not None or tag_2 is not None or tag_3 is not None:
        recipe_list = Favourites.objects.filter(
            user__username=username
            ).filter(Q(recipe__tag__tag=tag_1) | Q(recipe__tag__tag=tag_2) | Q(recipe__tag__tag=tag_3))#.order_by('pecipe.-pub_date')
    return recipe_list
   