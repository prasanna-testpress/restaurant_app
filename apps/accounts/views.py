from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from apps.accounts.forms import SignupForm, LoginForm, ProfileUpdateForm


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["profile_user"] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profiles/profile_edit.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'password_form' not in context:
            context['password_form'] = PasswordChangeForm(user=self.request.user)
        context['profile_form'] = context['form'] 
        return context


class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "profiles/profile_edit.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'profile_form' not in context:
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user)
        context['password_form'] = context['form']
        return context

