from rest_framework import serializers
from app.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')


# class FovouritesS(serializers.Serializer):

#     def validate(self, date):
#         created = Favourites.objects.get_or_create(
#             user_id=request.user.id, recipe_id=data['id']
#         )
#         if created:
#             return {'success': True}
#         else:
#             return {'success': False}