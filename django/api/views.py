from rest_framework.generics import ListAPIView

from mercari import models
from . import serializers

# Create your views here.


class CategoryList(ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = models.Category.objects\
            .filter(descendant_category__parent=category_id)

        return queryset
