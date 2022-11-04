from .views import CreateUserView, CreateTokenView, ManageUserView
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('token/', CreateTokenView.as_view(), name='token')
]
