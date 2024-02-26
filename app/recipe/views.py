from .serializers import RecipeSerializer
from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet
from core.models import Recipe


class RecipeViews(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# w3e4yhwehb
#kurczak
