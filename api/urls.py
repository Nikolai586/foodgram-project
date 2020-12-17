from django.urls import path
from .views import (
    favourites_del,
    favourites_add,
    purchases_add,
    purchases_del,
    subscriptions_add,
    subscriptions_del,
    subscriptions_del_name,
    GetIngredient,
)

urlpatterns = [
    path('ingredients', GetIngredient.as_view()),
    path('favorites/<int:id>', favourites_del),
    path('favorites', favourites_add),
    path('subscriptions', subscriptions_add),
    path('subscriptions/<int:id>', subscriptions_del),
    path('purchases', purchases_add),
    path('purchases/<int:id>', purchases_del),
    path('subscript/<str:username>', subscriptions_del_name),
]
