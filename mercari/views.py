from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from . import forms
from . import models


# Create your views here.


class ItemListView(LoginRequiredMixin, ListView, FormMixin):
    model = models.Item
    template_name = 'list.html'
    paginate_by = 30
    form_class = forms.SearchForm

    def get_queryset(self):

        form = forms.SearchForm(
            data=self.request.GET,
        )

        form.data.name = form.data.get('name') or ''
        form.data.brand = form.data.get('brand') or ''
        form.data.category = form.data.get('category') or ''

        depth_1_category = form.data.get('depth_1_category')
        if depth_1_category != '' and depth_1_category is not None:
            form.data.category = depth_1_category

        depth_2_category = form.data.get('depth_2_category')
        if depth_2_category != '' and depth_2_category is not None:
            form.data.category = depth_2_category

        depth_3_category = form.data.get('depth_3_category')
        if depth_3_category != '' and depth_3_category is not None:
            form.data.category = depth_3_category

        # category で 検索している場合
        if form.data.category != '' and form.data.category is not None:
            depth = models.ClosureTreeCategory.objects \
                .get(closure_tree_category_id=form.data.category).depth

            if depth == 1:
                return models.Item.objects \
                    .order_by('item_id') \
                    .filter(
                    name__contains=form.data.name,
                    brand__contains=form.data.brand,
                    category__parent__parent_id=form.data.category,
                )

            elif depth == 2:
                return models.Item.objects \
                    .order_by('item_id') \
                    .filter(
                    name__contains=form.data.name,
                    brand__contains=form.data.brand,
                    category__parent_id=form.data.category,
                )

            elif depth == 3:
                return models.Item.objects \
                    .order_by('item_id') \
                    .filter(
                    name__contains=form.data.name,
                    brand__contains=form.data.brand,
                    category__descendant__category_id=form.data.category,
                )
        else:
            return models.Item.objects \
                .order_by('item_id') \
                .filter(
                name__contains=form.data.name,
                brand__contains=form.data.brand,
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        print('********** get context data***************')
        context = super().get_context_data(**kwargs)

        # 検索フォームをインスタンス化
        form = forms.SearchForm(self.request.GET)

        # カテゴリー検索 depth1
        depth_1_category_list = list(models.Category.objects.filter(
            descendant_category__depth=1).values_list())
        depth_1_category_list.insert(0, (None, '==========',))
        form.fields['depth_1_category'].choices = depth_1_category_list

        # 最終的にcategory検索に使用するid
        category = None

        depth_1_category = form.data.get('depth_1_category')
        if depth_1_category or depth_1_category == '':
            form.fields['depth_1_category'].initial = depth_1_category
            category = depth_1_category

        # depth 2
        depth_2_category = form.data.get('depth_2_category')
        depth_2_category_list = None

        if depth_2_category or depth_2_category == '':
            depth_2_category_list = list(models.Category.objects \
                                         .order_by('category_id') \
                                         .filter(descendant_category__parent=2).values_list())

        else:
            category = depth_2_category
            depth_2_category_list = list(models.Category.objects \
                                         .order_by('category_id') \
                                         .filter(
                descendant_category__parent=depth_1_category).values_list())
            form.fields['depth_2_category'].initial = depth_2_category

        depth_2_category_list.insert(0, (None, '==========',))
        form.fields['depth_2_category'].choices = depth_2_category_list

        # depth 3
        depth_3_category = form.data.get('depth_3_category')
        depth_3_category_list = None
        if depth_3_category or depth_3_category == '':
            # FIXME 29は適当な初期値
            depth_3_category_list = list(models.Category.objects \
                                         .order_by('category_id') \
                                         .filter(descendant_category__parent=29).values_list())


        else:
            category = depth_3_category
            depth_3_category_list = list(models.Category.objects \
                                         .order_by('category_id') \
                                         .filter(
                descendant_category__parent=depth_2_category).values_list())
            form.fields['depth_3_category'].initial = depth_3_category

        depth_3_category_list.insert(0, (None, '==========',))
        form.fields['depth_3_category'].choices = depth_3_category_list

        if category:
            form.data.category = category

        context['form'] = form

        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = models.Item
    template_name = 'detail.html'


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Item
    template_name = 'edit.html'


@login_required
def item_update_view(request, pk):
    if request.method == "GET":
        item = get_object_or_404(models.Item, pk=pk)
        item_category_id_depth_3 = item.category.descendant.category_id
        item_category_id_depth_2 = item.category.parent.descendant.category_id
        item_category_id_depth_1 = item.category.parent.parent.descendant \
            .category_id

        # =====================depth 3 category=====================
        depth_3_category_list = models.Category.objects.filter(
            descendant_category__parent=item_category_id_depth_2).values_list()

        # =====================depth 2 category=====================
        depth_2_category_list = models.Category.objects.filter(
            descendant_category__parent=item_category_id_depth_1).values_list()

        # =====================depth 1 category=====================
        depth_1_category_list = models.Category.objects.filter(
            descendant_category__depth=1).values_list()

        initial = {
            'depth_3_category': item_category_id_depth_3,
            'depth_2_category': item_category_id_depth_2,
            'depth_1_category': item_category_id_depth_1,
            'condition': item.condition,
            'shipping': item.shipping
        }

        form = forms.ItemUpdateForm(
            instance=item,
            initial=initial,
            depth_3_category_list=depth_3_category_list,
            depth_2_category_list=depth_2_category_list,
            depth_1_category_list=depth_1_category_list
        )

        data = {
            'form': form,
            'pk': pk
        }

        if request.GET.get('error') == 'category':
            data['error'] = 'カテゴリーをすべて正しく選択してください。'

        return render(request, 'edit.html', data)

    else:
        form = forms.ItemUpdateForm(
            data=request.POST,
            initial=None,
            depth_3_category_list=None,
            depth_2_category_list=None,
            depth_1_category_list=None
        )

        if form.is_valid:

            if form.data.get('depth_3_category') == '' or \
                    form.data.get('depth_2_category') == '' or \
                    form.data.get('depth_1_category') == '':
                return redirect(reverse('edit', kwargs={'pk': pk}) + '?error=category')

            category = models.ClosureTreeCategory.objects.get(
                depth=3,
                descendant=request.POST.get('depth_3_category'),
                parent__isnull=False)

            item = models.Item(
                item_id=pk,
                name=request.POST.get('name'),
                condition=request.POST.get('condition'),
                category=category,
                brand=request.POST.get('brand'),
                price=request.POST.get('price'),
                shipping=request.POST.get('shipping'),
                description=request.POST.get('description'), )
            item.save()
            return redirect('detail', pk=pk)

        else:
            return render(request, 'edit.html', {'form': form})


@login_required
def item_create_view(request):
    if request.method == "GET":

        form = forms.ItemCreateForm()

        data = {
            'form': form,
        }

        if request.GET.get('error') == 'category':
            data['error'] = 'カテゴリーをすべて正しく選択してください。'

        return render(request, 'create.html', data)

    else:
        form = forms.ItemCreateForm(data=request.POST)

        if form.is_valid:

            if form.data.get('depth_3_category') == '' or \
                    form.data.get('depth_2_category') == '' or \
                    form.data.get('depth_1_category') == '':
                return render(request, 'create.html', {'form': form, 'error': 'カテゴリーを正しく選択してください'})

            category = models.ClosureTreeCategory.objects.get(
                depth=3,
                descendant=request.POST.get('depth_3_category'),
                parent__isnull=False)

            item = models.Item(
                name=request.POST.get('name'),
                condition=request.POST.get('condition'),
                category=category,
                brand=request.POST.get('brand'),
                price=request.POST.get('price'),
                shipping=request.POST.get('shipping'),
                description=request.POST.get('description'), )
            item.save()
            return redirect('detail', pk=item.pk)

        else:
            return render(request, 'create.html', {'form': form})
