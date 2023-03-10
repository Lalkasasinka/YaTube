from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel


User = get_user_model()
POST_STR_MULTIPLIER = 15        # Ограничение текста в 15 символов.


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'


class Post(CreatedModel):
    text = models.TextField('Текст поста',
                            help_text='Введите текст поста')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              verbose_name='Группа',
                              related_name='posts',
                              help_text='Группа, к которой '
                                        'будет относиться пост')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:POST_STR_MULTIPLIER]

    class Meta:
        verbose_name = 'Постики'
        verbose_name_plural = 'Постики'
        ordering = ['-pub_date']


class Comment(CreatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    text = models.TextField('Комментарий')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
