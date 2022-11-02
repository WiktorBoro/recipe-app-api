from .views import CreateUserView, CreateTokenView, ManageUserView
from rest_framework import routers
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('token/', CreateTokenView.as_view(), name='token')
]
