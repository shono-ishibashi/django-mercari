from django.urls import path
from . import views


urlpatterns = [
    path('get_parent_categroy/<int:category_id>',
         views.CategoryList.as_view()
         )
]
