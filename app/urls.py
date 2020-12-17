from django.urls import path
from .views import (
    Index,
    single,
    author_ricipe,
    favourites,
    subscriptions_list,
    purchases,
    purchases_file,
    purchases_del_not_js,
    create_recipe,
    recipe_edit,
    delete_recipe,
)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create/', create_recipe, name='create'),
    path('<str:username>/<int:id>/edit/', recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:id>/del/', delete_recipe, name='del_recipe'),
    path('purchases/del/<int:id>', purchases_del_not_js, name='purchases_del_not_js'),
    path('purchases_shop/', purchases, name='purchases'),
    path('purchases_file/', purchases_file, name='purchases_file'),
    path('follow/', subscriptions_list, name='follow'),
    path('favourites/', favourites, name='favourites'),
    path('<str:username>/', author_ricipe, name='author_recipe'),
    path('index/<int:recipe_id>/', single, name='single'),
]
