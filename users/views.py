from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, DetailView, ListView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from main.models import Publications
from .forms import ProfileUserForm, RegisterUserForm, CustomAuthenticationForm
from .models import Profile, Follow


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")


class ProfileUserView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        try:
            if self.kwargs.get("username"):
                return get_user_model().objects.get(username=self.kwargs["username"])
            return self.request.user
        except get_user_model().DoesNotExist:
            raise Http404("User does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Publications.objects.filter(author=user)
        context['liked_posts'] = Publications.objects.filter(likes=user)
        context['user_following'] = Follow.objects.filter(user=self.request.user, author=user).exists()
        context['background_color'] = user.profile.background_color  # Add background color to context
        return context

    def get_template_names(self):
        if self.request.user.username == self.kwargs.get("username", self.request.user.username):
            return ["users/profile.html"]
        return ["users/user_profile.html"]



class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUserForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        profile = form.save(commit=False)
        user = profile.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        if 'avatar' in form.cleaned_data and form.cleaned_data['avatar']:
            profile.avatar = form.cleaned_data['avatar']
        if 'birth_date' in form.cleaned_data and form.cleaned_data['birth_date']:
            profile.birth_date = form.cleaned_data['birth_date']
        user.save()
        profile.save()
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = User
    template_name = "users/user_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Publications.objects.filter(author=user)
        return context


class FollowersListView(LoginRequiredMixin, ListView):
    template_name = 'users/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Follow.objects.filter(author=user)

class FollowingListView(LoginRequiredMixin, ListView):
    template_name = 'users/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Follow.objects.filter(user=user)


class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, username=kwargs.get("username"))

        follow_instance, created = Follow.objects.get_or_create(user=request.user, author=user_to_follow)

        if not created:
            follow_instance.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
