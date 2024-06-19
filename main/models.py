from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Publications(models.Model):
    image = models.ImageField("Изображение", upload_to="images/")
    title = models.CharField("Описание", max_length=250)
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        null=True,
        related_name="posts",
    )
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    cat = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория"
    )
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse(
            "main:post", kwargs={"cat_slug": self.cat.slug, "post_slug": self.slug}
        )

    def total_likes(self):
        return self.likes.count()


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:category", kwargs={"cat_slug": self.slug})


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Publications,
        verbose_name="Пост",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(
        verbose_name="Текст", max_length=1000, null=True, blank=True
    )

    class Meta:
        ordering = ["datetime"]


