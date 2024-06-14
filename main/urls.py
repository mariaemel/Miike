from django.urls import path

from .views import (
    AddCommentView,
    ArticlesView,
    CategoryView,
    CompilationView,
    CreatePublicationView,
    DeleteCommentView,
    EditCommentView,
    IndexView,
    PostDetailView,
    SearchView,
    UpdatePublicationView,
    DeletePublicationView,
    LikePostView,
    ConfirmDeletePublicationView,
)

app_name = "main"


urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("compilations/", CompilationView.as_view(), name="compilations"),
    path("articles/", ArticlesView.as_view(), name="articles"),
    path("create/", CreatePublicationView.as_view(), name="create"),
    path("upload/", CreatePublicationView.as_view()),
    path("post/<slug:cat_slug>/<slug:post_slug>/", PostDetailView.as_view(), name="post"),
    path("category/", CategoryView.as_view(), name="all_categories"),
    path("category/<slug:cat_slug>/", CategoryView.as_view(), name="category"),
    path("comment/add/<int:pk>/", AddCommentView.as_view(), name="add_comment"),
    path("comment/edit/<int:pk>/", EditCommentView.as_view(), name="edit_comment"),
    path("comment/delete/<int:pk>/", DeleteCommentView.as_view(), name="delete_comment"),
    path('search/', SearchView.as_view(), name='search'),
    path("post/<slug:cat_slug>/<slug:post_slug>/update/", UpdatePublicationView.as_view(), name="update"),
    path("post/<slug:cat_slug>/<slug:post_slug>/confirm_delete/", ConfirmDeletePublicationView.as_view(), name="confirm_delete"),
    path("post/<slug:cat_slug>/<slug:post_slug>/delete/", DeletePublicationView.as_view(), name="delete"),
    path('like/', LikePostView.as_view(), name='like_post'),
]