from django.template.context_processors import request
from recipe.models import Purchases

def menu(request):
    recipe_bay_count = Purchases.objects.filter(user__username=request.user).count()
    return {'recipe_bay_count': recipe_bay_count}