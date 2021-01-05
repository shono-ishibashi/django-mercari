from django import forms

from . import models
from .validator import validate_category


class ItemUpdateForm(forms.ModelForm):
    item_id = forms.HiddenInput()
    name = forms.CharField(max_length=100, required=True)
    condition = forms.ChoiceField(
        choices=((1, 1), (2, 2), (3, 3)),
        required=True,
    )

    shipping = forms.ChoiceField(
        choices=((0, 0), (1, 1), (2, 2)),
        required=True,
    )

    depth_3_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )
    depth_2_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )
    depth_1_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )

    field_order = ['item_id', 'name', 'brand', 'condition',
                   'depth_1_category', 'depth_2_category',
                   'depth_3_category', 'price', 'shipping', 'description']

    def __init__(self,
                 depth_3_category_list,
                 depth_2_category_list,
                 depth_1_category_list,
                 initial,
                 *args,
                 **kwargs):
        super(ItemUpdateForm, self).__init__(*args, **kwargs)

        # categeryのselect内のoptionを追加
        if depth_3_category_list:
            self.fields['depth_3_category'].choices = depth_3_category_list
        if depth_2_category_list:
            self.fields['depth_2_category'].choices = depth_2_category_list
        if depth_1_category_list:
            self.fields['depth_1_category'].choices = depth_1_category_list

        # categoryを選択済みにする
        if initial:
            self.fields['depth_3_category'].initial = \
                initial['depth_3_category']
            self.fields['depth_2_category'].initial = \
                initial['depth_2_category']
            self.fields['depth_1_category'].initial = \
                initial['depth_1_category']
            self.fields['condition'].initial = initial['condition']

        # templateにformにid属性をつける
        self.fields['depth_3_category'].widget.attrs['id'] = 'depth_3_category'
        self.fields['depth_2_category'].widget.attrs['id'] = 'depth_2_category'
        self.fields['depth_1_category'].widget.attrs['id'] = 'depth_1_category'

        # class='form-control'を追加
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Item
        fields = ('item_id', 'name', 'brand',
                  'price', 'shipping', 'description')


class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    brand = forms.CharField(max_length=100, required=False)
    depth_1_category = forms.ChoiceField(required=False)
    depth_2_category = forms.ChoiceField(required=False)
    depth_3_category = forms.ChoiceField(required=False)
    category = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['depth_3_category'].widget.attrs['id'] = 'depth_3_category'
        self.fields['depth_2_category'].widget.attrs['id'] = 'depth_2_category'
        self.fields['depth_1_category'].widget.attrs['id'] = 'depth_1_category'


class ItemCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    condition = forms.ChoiceField(
        choices=((1, 1), (2, 2), (3, 3)),
        required=True,
    )

    shipping = forms.ChoiceField(
        choices=((0, 0), (1, 1), (2, 2)),
        required=True,
    )

    depth_3_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )
    depth_2_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )
    depth_1_category = forms.ChoiceField(
        validators=[validate_category],
        required=True,
    )

    field_order = ['item_id', 'name', 'brand', 'condition',
                   'depth_1_category', 'depth_2_category',
                   'depth_3_category', 'price', 'shipping', 'description']

    def __init__(self,
                 *args,
                 **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)

        # categeryのselect内のoptionを追加
        self.fields['depth_1_category'].choices = models.Category.objects.filter(
            descendant_category__depth=1).values_list()

        # templateにformにid属性をつける
        self.fields['depth_3_category'].widget.attrs['id'] = 'depth_3_category'
        self.fields['depth_2_category'].widget.attrs['id'] = 'depth_2_category'
        self.fields['depth_1_category'].widget.attrs['id'] = 'depth_1_category'

        # class='form-control'を追加
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Item
        fields = ('item_id', 'name', 'brand',
                  'price', 'shipping', 'description')
