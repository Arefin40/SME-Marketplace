from django import forms
from .models import Product
from apps.stores.models import Collection


class ProductForm(forms.ModelForm):
    new_collection_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "New Collection Name"}),
    )

    class Meta:
        model = Product
        fields = ["name", "category", "collection", "description", "price", "stock", "sku", "image"]
        common_attrs = {"class": "input", "autocomplete": "off"}
        widgets = {
            "name": forms.TextInput(attrs={**common_attrs, "placeholder": "Product Name"}),
            "sku": forms.TextInput(attrs={**common_attrs, "placeholder": "SKU"}),
            "category": forms.TextInput(attrs={"class": "input", "placeholder": "Category"}),
            "price": forms.NumberInput(attrs={"class": "input", "placeholder": "Price"}),
            "stock": forms.NumberInput(attrs={"class": "input", "placeholder": "Stock"}),
            "collection": forms.Select(
                attrs={"class": "input", "placeholder": "Select Existing Collection"}
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "absolute inset-0 opacity-0",
                    "onchange": "showImage(event, '.main-image-preview')",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "input no-ring",
                    "rows": 12,
                    "placeholder": "Write a short description about the product",
                }
            ),
        }
        error_messages = {
            "name": {"required": "Product name is required."},
            "category": {"required": "Category is required."},
            "description": {"required": "Description is required."},
            "price": {"required": "Price is required."},
            "stock": {"required": "Stock quantity is required."},
            "sku": {"required": "SKU is required."},
            "image": {"required": "Image is required."},
        }

    # Show collections of the current merchant's store only
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["collection"].required = False
            self.fields["collection"].queryset = Collection.objects.filter(
                store__merchant=self.user
            )

    def clean(self):
        cleaned_data = super().clean()
        # Validate collection
        collection = cleaned_data.get("collection")
        new_collection_name = cleaned_data.get("new_collection_name")
        if not collection and not new_collection_name:
            self.add_error("new_collection_name", "Please select or create a collection")
        return cleaned_data
