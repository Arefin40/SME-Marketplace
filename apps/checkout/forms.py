from django import forms
from apps.users.models import Zone, Area


class CheckoutForm(forms.Form):
    # Shipping fields
    shipping_name = forms.CharField(
        label="Full Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Shipping name is required"},
    )
    shipping_contact = forms.CharField(
        label="Phone",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Shipping contact is required"},
    )
    shipping_address = forms.CharField(
        label="Address",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Shipping address is required"},
    )
    shipping_zone = forms.ModelChoiceField(
        label="Zone",
        queryset=Zone.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "input", "onchange": "getAreas(event)"}),
        empty_label="Select zone",
        error_messages={"required": "Please select a zone"},
    )
    shipping_area = forms.ModelChoiceField(
        label="Area",
        queryset=Area.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "input"}),
        empty_label="Select area",
        error_messages={"required": "Please select an area"},
    )

    # Billing fields
    billing_name = forms.CharField(
        label="Full Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Billing name is required"},
    )
    billing_contact = forms.CharField(
        label="Phone",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Billing contact is required"},
    )
    billing_address = forms.CharField(
        label="Address",
        required=True,
        widget=forms.TextInput(attrs={"class": "input"}),
        error_messages={"required": "Billing address is required"},
    )
    billing_zone = forms.ModelChoiceField(
        label="Zone",
        queryset=Zone.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "input", "onchange": "getAreas(event)"}),
        empty_label="Select zone",
        error_messages={"required": "Please select a zone"},
    )
    billing_area = forms.ModelChoiceField(
        label="Area",
        queryset=Area.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "input"}),
        empty_label="Select area",
        error_messages={"required": "Please select an area"},
    )

    # Shipping method
    shipping_method = forms.ChoiceField(
        label="Shipping Method",
        choices=[("STANDARD", "Standard Delivery"), ("EXPRESS", "Express Delivery")],
        required=True,
        widget=forms.RadioSelect(
            attrs={
                "name": "shipping_method",
                "class": "peer sr-only",
                "onchange": "updateShippingPrice(event)",
            }
        ),
        error_messages={"required": "Please select a shipping method"},
        initial="STANDARD",
    )

    def __init__(self, *args, **kwargs):
        # Extract the zone data from the form data if available
        kwargs.pop("shipping_zone", None)
        kwargs.pop("billing_zone", None)
        super().__init__(*args, **kwargs)

        # Filter shipping_area based on shipping_zone in form data
        if "shipping_zone" in self.data:
            try:
                zone_id = int(self.data.get("shipping_zone"))
                self.fields["shipping_area"].queryset = Area.objects.filter(district_id=zone_id)
            except (ValueError, TypeError):
                self.fields["shipping_area"].queryset = Area.objects.none()
        else:
            self.fields["shipping_area"].queryset = Area.objects.none()

        # Filter billing_area based on billing_zone in form data
        if "billing_zone" in self.data:
            try:
                zone_id = int(self.data.get("billing_zone"))
                self.fields["billing_area"].queryset = Area.objects.filter(district_id=zone_id)
            except (ValueError, TypeError):
                self.fields["billing_area"].queryset = Area.objects.none()
        else:
            self.fields["billing_area"].queryset = Area.objects.none()
