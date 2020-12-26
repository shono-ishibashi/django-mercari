from django.views.generic import ListView, DetailView, UpdateView

from . import models

# Create your views here.


class ItemListView(ListView):
    model = models.Item
    template_name = 'list.html'
    paginate_by = 30
    ordering = 'item_id'

    # def get_queryset(self):
    #     item_list = models.Item.objects\
    #         .select_related('category')\
    #         .filter(category__isnull=False)\
    #         .all()\
    #         .order_by('category')
    #     return item_list

    # def get_queryset(self):
    #     item_list = models.Item.objects\
    #         .select_related('category')\
    #         .filter(category__isnull=False)\
    #         .all()\
    #         .order_by('pk')

    #     for item in item_list:
    #         print('####################################')
    #         print('depth3:', item.category.descendant.name)
    #         print('depth2:', item.category.parent.descendant.name)
    #         print('depth1:', item.category.parent.parent.descendant.name)
    #         print('####################################')
    #         print(vars(item))

    #     return item_list


class ItemDetailView(DetailView):
    model = models.Item
    template_name = 'detail.html'


class ItemUpdateView(UpdateView):
    model = models.Item
    template_name = 'edit.html'
