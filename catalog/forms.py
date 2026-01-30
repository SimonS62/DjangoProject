from django import forms
from .models import Product


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def clean_name(self):
        """Проверяет отсутствие запрещенных слов в названии."""
        name = self.cleaned_data.get('name')
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"Название содержит запрещенное слово: '{word}'.")
        return name

    def clean_description(self):
        """Проверяет отсутствие запрещенных слов в описании."""
        description = self.cleaned_data.get('description')
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f"Описание содержит запрещенное слово: '{word}'.")
        return description

    def clean_price(self):
        """Валидирует, что цена не отрицательная."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'}) # Стиль для чекбокса
