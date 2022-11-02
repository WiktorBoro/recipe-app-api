from rest_framework import serializers
from core import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = ['user', 'title', 'time_minutes', 'price', 'description', 'link']
        extra_kwargs = {'link': {'read_only': True}}

    def create(self, validated_data):
        recipe = models.Recipe().objects.create(**validated_data)
        return recipe

    def update(self, instance, validated_data):
        recipe = super().update(instance, validated_data)

        return recipe
