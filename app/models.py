from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Ingredient(models.Model):
    title = models.CharField(max_length=70)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Quantity(models.Model):
    ingr = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        blank=True, null=True
        )
    quantity = models.IntegerField()

    def __int__(self):
        return self.ingr

    def __str__(self):
        return '%s' % (self.ingr)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    tag = models.ManyToManyField(Tag, blank=True)
    quantity = models.ManyToManyField(Quantity, blank=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.title


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
        )


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
