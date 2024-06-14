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
from .forms import ProfileUserForm, RegisterUserForm
from .models import Profile


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")


class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_success_url(self):
        return reverse_lazy("users:profile")

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
        context['followers'] = user.profile.total_followers()
        context['following'] = user.following.count()  # Correctly count the number of followings
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
        user.save()
        profile.save()
        return super().form_valid(form)



class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, username=kwargs.get("username"))
        profile = user_to_follow.profile

        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
    model = User
    template_name = 'users/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return user.profile.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username'])
        return context

class FollowingListView(ListView):
    model = User
    template_name = 'users/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        following = user.profile.followers.all()  # Access followers through Profile model
        return following

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username'])
        return context

