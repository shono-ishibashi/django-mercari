from rest_framework import serializers
from mercari import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item


class ClosureTreeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClosureTreeCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
