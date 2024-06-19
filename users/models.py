from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/profile/',
        default='main/img/hum.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))]
    )
    bio = models.TextField(null=True, max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    background_color = models.CharField(max_length=7, default='#BA9797', verbose_name='Цвет фона')

    def __str__(self):
        return self.user.username

    def total_followers(self):
        return Follow.objects.filter(author=self.user).count()

    def total_following(self):
        return Follow.objects.filter(user=self.user).count()



class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'


