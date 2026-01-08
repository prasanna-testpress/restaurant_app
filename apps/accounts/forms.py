from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


# -------------------------------------------------
# 1. MIXIN FOR TAILWIND STYLES
# -------------------------------------------------
class StyledFormMixin:
    """
    Mixin to automatically apply Tailwind CSS classes to all form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_classes = (
            "w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 "
            "text-gray-800 placeholder-gray-400 focus:outline-none "
            "focus:border-brand focus:ring-4 focus:ring-brand/10 "
            "transition duration-200"
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = default_classes


# -------------------------------------------------
# 2. SIGNUP FORM
# -------------------------------------------------
class SignupForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-enter your password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email address",
                    "autocomplete": "email",
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "Passwords do not match. Please try again.",
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# -------------------------------------------------
# 3. LOGIN FORM
# -------------------------------------------------
class LoginForm(StyledFormMixin, forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data

        self.user = authenticate(
            request=self.request,
            username=email,
            password=password,
        )

        if self.user is None:
            raise forms.ValidationError(
                "Invalid email or password. Please try again."
            )

        if not self.user.is_active:
            raise forms.ValidationError(
                "Invalid email or password. Please try again."
            )

        return cleaned_data

    def get_user(self):
        return self.user
