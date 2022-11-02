from django.shortcuts import render
from rest_framework import permissions, authentication
from rest_framework.viewsets import ViewSet


class RecipePublicViews(ViewSet):
    serializer_class = UserSerializer
    http_method_names = ['GET']


class RecipePrivateViews(ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

