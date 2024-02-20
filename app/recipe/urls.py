from .views import RecipeViews
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'recipes'

router = DefaultRouter(trailing_slash=False)

router.register('', RecipeViews, basename='recipes')

urlpatterns = router.urls
# ok
