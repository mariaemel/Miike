from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from .forms import CommentForm, PublicationsForm, SearchForm
from .models import Category, Comment, Publications


class BasePageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, "page_title"):
            context["title"] = self.page_title

        return context


class IndexView(BasePageView):
    template_name = "main/index.html"
    page_title = "Главная страница"


class ArticlesView(BasePageView):
    template_name = "main/articles.html"
    page_title = "Образовательный контент"


class CreatePublicationView(LoginRequiredMixin, CreateView):
    model = Publications
    form_class = PublicationsForm
    template_name = "main/create.html"
    success_url = reverse_lazy("main:compilations")

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class CompilationView(ListView):
    model = Publications
    template_name = "main/compilations.html"
    context_object_name = "posts"

    def get_ordering(self):
        return '-id'


class CategoryView(CompilationView):
    def get_queryset(self):
        self.category = None
        if "cat_slug" in self.kwargs:
            self.category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])

            return Publications.objects.filter(cat=self.category)

        return Publications.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category

        return context



class PostDetailView(DetailView):
    model = Publications
    template_name = "main/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["cat_selected"] = self.object.cat.id
        context["comment_form"] = CommentForm()
        context["total_likes"] = self.object.total_likes()
        context["liked_users"] = self.object.likes.all()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'like' in request.POST:
            if request.user in self.object.likes.all():
                self.object.likes.remove(request.user)
            else:
                self.object.likes.add(request.user)
        return redirect('main:post', cat_slug=self.object.cat.slug, post_slug=self.object.slug)


class BaseCommentView:
    model = Comment

    def get_success_url(self):
        post = Publications.objects.get(pk=self.object.post.pk)
        return reverse(
            "main:post", kwargs={"cat_slug": post.cat.slug, "post_slug": post.slug}
        )


class AddCommentView(BaseCommentView, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Publications.objects.get(pk=self.kwargs.get("pk"))
        return super().form_valid(form)


class EditCommentView(BaseCommentView, UpdateView):
    form_class = CommentForm
    template_name = "main/comment_edit.html"


class DeleteCommentView(BaseCommentView, DeleteView):
    template_name = "main/comment_delete.html"


class SearchView(ListView):
    model = Publications
    template_name = 'main/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Publications.objects.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query) | Q(cat__name__icontains=query)
            )
        return Publications.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['form'] = SearchForm(initial={'query': context['query']})
        return context


class UpdatePublicationView(LoginRequiredMixin, UpdateView):
    model = Publications
    form_class = PublicationsForm
    template_name = "main/update.html"
    success_url = reverse_lazy("main:compilations")

    def get_object(self, queryset=None):
        return get_object_or_404(Publications, slug=self.kwargs.get('post_slug'))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePublicationView(DeleteView):
    model = Publications
    success_url = reverse_lazy('main:compilations')
    template_name = 'main/delete.html'
    slug_url_kwarg = 'post_slug'


class ConfirmDeletePublicationView(LoginRequiredMixin, DetailView):
    model = Publications
    template_name = 'main/confirm_delete.html'
    slug_url_kwarg = 'post_slug'


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Publications, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        else:
            return JsonResponse({'redirect': reverse('users:login')})
