from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "autocomplete": "new-password"}
        ),
        error_messages={
            "required": "Please enter a password",
        },
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-enter your password",
                "autocomplete": "new-password",
            }
        ),
        error_messages={
            "required": "Please confirm your password",
        },
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
        error_messages = {
            "email": {
                "required": "Please enter your email address",
                "invalid": "Please enter a valid email address",
                "unique": "An account with this email already exists",
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email address", "autocomplete": "email"}
        ),
        error_messages={
            "required": "Please enter your email address",
            "invalid": "Please enter a valid email address",
        },
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
        error_messages={
            "required": "Please enter your password",
        },
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )
            if not self.user.is_active:
                raise forms.ValidationError("This account has been deactivated.")

        return cleaned_data

    def get_user(self):
        return self.user
