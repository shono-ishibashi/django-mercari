from django import forms

from . import models


class ItemUpdateForm(forms.ModelForm):
    item_id = forms.HiddenInput()
    name = forms.CharField(max_length=100, required=True)
    condition = forms.ChoiceField(
        choices=((1, 1), (2, 2), (3, 3)),
        required=True,
    )

    depth_3_category = forms.ChoiceField(required=True)
    depth_2_category = forms.ChoiceField(required=True)
    depth_1_category = forms.ChoiceField(required=True)

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
        self.fields['depth_3_category'].choices = depth_3_category_list
        self.fields['depth_2_category'].choices = depth_2_category_list
        self.fields['depth_1_category'].choices = depth_1_category_list

        # DBに登録しているcategoryを選択済みにする
        self.fields['depth_3_category'].initial = initial['depth_3_category']
        self.fields['depth_2_category'].initial = initial['depth_2_category']
        self.fields['depth_1_category'].initial = initial['depth_1_category']

        # class='form-control'を追加
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Item
        fields = ('item_id', 'name', 'brand',
                  'price', 'shipping', 'description')
