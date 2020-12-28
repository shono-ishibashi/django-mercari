from django.urls import path
from . import views


urlpatterns = [
    path('', views.ItemListView.as_view(), name='list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detail'),
    # path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='edit'),
    path('<int:item_id>/edit/', views.item_update_view, name='edit'),
]
