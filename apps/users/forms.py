from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import password_validators_help_texts
from .models import MerchantApplication, Address, Area, Zone

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    fname = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your first name",
                "autocomplete": "given-name",
            }
        ),
        required=True,
        error_messages={"required": "First name is required."},
    )
    lname = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your last name",
                "autocomplete": "family-name",
            }
        ),
        required=True,
        error_messages={"required": "Last name is required."},
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your email",
                "autocomplete": "email",
            }
        ),
        required=True,
        error_messages={"required": "Email is required."},
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "password-field pr-10 w-full",
                "placeholder": "Enter a password",
            }
        ),
        required=True,
        error_messages={"required": "Password is required."},
        help_text=password_validators_help_texts(),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "password-field pr-10 w-full",
                "placeholder": "Enter the password again",
            }
        ),
        required=True,
        error_messages={"required": "Confirm password is required."},
    )

    class Meta:
        model = User
        fields = ["fname", "lname", "email", "password", "confirm_password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.name = f"{self.cleaned_data.get('fname')} {self.cleaned_data.get('lname')}"
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class UserSignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input w-full pl-10",
                "placeholder": "Enter email",
                "autocomplete": "email",
            }
        ),
        required=True,
        error_messages={"required": "Email is required."},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "password-field w-full px-10",
                "placeholder": "Enter password",
            }
        ),
        required=True,
        error_messages={"required": "Password is required."},
    )


class BecomeMerchantForm(forms.ModelForm):
    photo = forms.FileField(
        label="Photo",
        widget=forms.FileInput(
            attrs={
                "class": "absolute inset-0 appearance-none opacity-0 outline-none focus:outline-none focus:ring-0",
                "accept": "image/*",
                "onchange": "showImage(event)",
            }
        ),
        required=True,
        error_messages={"required": "Photo is required."},
    )

    nid = forms.CharField(
        label="NID",
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your NID",
                "autocomplete": "off",
            }
        ),
        required=True,
        error_messages={"required": "NID is required."},
    )

    contact = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your phone number",
                "autocomplete": "phone",
            }
        ),
        required=True,
        error_messages={"required": "Phone number is required."},
    )

    email = forms.EmailField(
        label="Business Email",
        widget=forms.EmailInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Enter your business email",
                "autocomplete": "email",
            }
        ),
        required=True,
        error_messages={"required": "Business email is required."},
    )

    class Meta:
        model = MerchantApplication
        fields = ["nid", "photo", "email", "contact"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        return email


class AddressForm(forms.ModelForm):
    zone = forms.ModelChoiceField(
        label="Zone",
        queryset=Zone.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "input", "onchange": "getAreasFromZone(event)"}),
        empty_label="Select zone",
        error_messages={"required": "Please select a zone"},
    )
    area = forms.ModelChoiceField(
        label="Area",
        queryset=Area.objects.none(),
        required=True,
        widget=forms.Select(attrs={"class": "input"}),
        empty_label="Select area",
        error_messages={"required": "Please select an area"},
    )

    class Meta:
        model = Address
        fields = ["label", "address", "area", "zone", "contact"]
        widgets = {
            "label": forms.TextInput(attrs={"class": "input", "placeholder": "Home, Office, etc."}),
            "address": forms.TextInput(attrs={"class": "input", "placeholder": "Street address"}),
            "contact": forms.TextInput(attrs={"class": "input", "placeholder": "Contact number"}),
        }
        error_messages = {
            "label": {"required": "Label is required."},
            "address": {"required": "Address is required."},
            "contact": {"required": "Contact number is required."},
        }

    def __init__(self, *args, **kwargs):
        # Extract the zone data from the form data if available
        kwargs.pop("zone", None)
        super().__init__(*args, **kwargs)

        if "zone" in self.data:
            try:
                zone_id = int(self.data.get("zone"))
                self.fields["area"].queryset = Area.objects.filter(district_id=zone_id)
            except (ValueError, TypeError):
                self.fields["area"].queryset = Area.objects.none()
        elif self.instance and self.instance.zone:
            self.fields["area"].queryset = Area.objects.filter(district=self.instance.zone)
