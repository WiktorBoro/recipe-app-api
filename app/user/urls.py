from .views import User
from rest_framework import routers

app_name = 'user'

router = routers.DefaultRouter(trailing_slash=False)
router.register('create', User, basename='create')

urlpatterns = router.urls
