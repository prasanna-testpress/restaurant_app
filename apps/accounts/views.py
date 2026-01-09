from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.views.generic import FormView

from apps.accounts.forms import SignupForm, LoginForm


class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
