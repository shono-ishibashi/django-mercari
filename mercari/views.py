from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView

from . import forms
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


def item_update_view(request, item_id):

    item = get_object_or_404(models.Item, pk=item_id)

    item_category_id_depth_3 = item.category.descendant.category_id
    item_category_id_depth_2 = item.category.parent.descendant.category_id
    item_category_id_depth_1 = item.category.parent.parent.descendant\
        .category_id

    # =====================depth 3 category=====================
    depth_3_category_list = models.Category.objects.filter(
        descendant_category__parent=item_category_id_depth_2).values_list()

    # =====================depth 2 category=====================
    depth_2_category_list = models.Category.objects\
        .filter(descendant_category__parent=item_category_id_depth_1)\
        .values_list()

    # =====================depth 1 category=====================
    depth_1_category_list = models.Category.objects\
        .filter(descendant_category__depth=1)\
        .values_list()

    initial = {
        'depth_3_category': item_category_id_depth_3,
        'depth_2_category': item_category_id_depth_2,
        'depth_1_category': item_category_id_depth_1
    }

    form = forms.ItemUpdateForm(instance=item,
                                initial=initial,
                                depth_3_category_list=depth_3_category_list,
                                depth_2_category_list=depth_2_category_list,
                                depth_1_category_list=depth_1_category_list
                                )

    return render(request, 'edit.html', {'form': form})
