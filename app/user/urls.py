from .views import CreateUserView, CreateTokenView
from rest_framework import routers
from django.urls import path

app_name = 'user'


urlpatterns = [
    path('create/', CreateUserView.as_view({'post': 'create'}), name='create'),
    path('me/', CreateUserView.as_view({'get': 'list', 'patch': 'update'}), name='me'),
    path('token/', CreateTokenView.as_view(), name='token')
]
