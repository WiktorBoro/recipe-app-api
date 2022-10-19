from rest_framework import viewsets
from .serializers import UserSerializer


class User(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['post']
    # permission_classes = [IsAccountAdminOrReadOnly]

