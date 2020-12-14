from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    Ingredient,
    Quantity,
    Favourites,
    Subscriptions,
    Purchases,
)

class PurchasesAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    empty_value_display = '-пусто-'

class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    empty_value_display = '-пусто-'

class FavouritesAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    empty_value_display = '-пусто-'

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'title', 'description', 'cooking_time']
    list_filter = ("pub_date",)
    empty_value_display = '-пусто-'

class IngredientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'dimension']
    empty_value_display = '-пусто-'

class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag']
    empty_value_display = '-пусто-'

class QuantityAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'ingr']


admin.site.register(Purchases, PurchasesAdmin)
admin.site.register(Quantity, QuantityAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(Tag, TagAdmin)    
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favourites, FavouritesAdmin)
