from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'description', 'link']
        extra_kwargs = {'id': {'read_only': True}}

    # def create(self, validated_data):
    #     recipe = Recipe.objects.create(**validated_data)
    #     return recipe
    ####
    # def update(self, instance, validated_data):
    #     recipe = super().update(instance, validated_data)
    #
    #     return recipe
