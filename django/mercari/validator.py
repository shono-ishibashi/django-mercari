from django import forms


def validate_category(value):
    if value == '':
        raise forms.ValidationError(
            "categoryを選択してください",
            params={'value': value}
        )
