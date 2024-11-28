from django import forms
from .models import Store


class CreateStoreForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-2 rounded-md border border-gray-300 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30 text-foreground",
                "placeholder": "Name of your business",
                "onchange": "syncText(event, 'store-name-preview', 'Store Name')",
                "oninput": "syncText(event, 'store-name-preview', 'Store Name')",
            }
        ),
        required=True,
        error_messages={"required": "Store name is required."},
    )

    slug = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Unique store identifier",
                "onchange": "syncText(event, 'store-slug-preview', 'storename')",
                "oninput": "syncText(event, 'store-slug-preview', 'storename')",
                "class": "w-full p-2 rounded-md border border-gray-300 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30 text-foreground",
            }
        ),
        required=True,
        error_messages={"required": "Store slug is required."},
    )

    logo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
                "onchange": "showImage(event, '.store-logo-preview')",
                "class": "absolute inset-0 opacity-0 z-10",
            },
        ),
        required=False,
    )

    cover = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
                "onchange": "showImage(event, '.store-cover-preview')",
                "class": "absolute inset-0 opacity-0 w-full h-full cursor-pointer z-10",
            }
        ),
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Describe your store",
                "rows": 4,
                "class": "w-full p-2 rounded-md border border-gray-300 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30 text-foreground",
            }
        ),
        required=False,
    )

    class Meta:
        model = Store
        fields = ["name", "slug", "logo", "cover", "description"]

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Store.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already taken.")
        return slug
