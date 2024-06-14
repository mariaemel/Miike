from django.urls import path
from .views import (
    LoginUser, RegisterUser, ProfileUserView, ProfileEditView,
    FollowToggleView, UserProfileView, FollowersListView, FollowingListView
)
from django.contrib.auth.views import PasswordChangeView, LogoutView

app_name = "users"

urlpatterns = [
    path("login/", LoginUser.as_view(next_page="main:home"), name="login"),
    path("logout/", LogoutView.as_view(next_page="main:home"), name="logout"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("profile/", ProfileUserView.as_view(), name="profile"),
    path("profile/<str:username>", ProfileUserView.as_view(), name="user_profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("follow-toggle/<str:username>/", FollowToggleView.as_view(), name="follow_toggle"),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('followers/<str:username>/', FollowersListView.as_view(), name='followers_list'),
    path('following/<str:username>/', FollowingListView.as_view(), name='following_list'),
]
