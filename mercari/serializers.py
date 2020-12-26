from rest_framework import serializers
from . import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item


class ClosureTreeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClosureTreeCategory
        fields = '__all__'
