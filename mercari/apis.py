from rest_framework import viewsets, routers
from . import models
from . import serializers


class ClosureTableRelationsViewSet(viewsets.ModelViewSet):
    queryset = models.ClosureTreeCategory.objects.all()
    serializer_class = serializers.ClosureTreeCategorySerializer


router = routers.DefaultRouter()
router.register('test', ClosureTableRelationsViewSet)
