from django.urls import path
from .views import SignUp

urlpatterns = [
    path('reg/', SignUp.as_view(), name='signup'),
]
