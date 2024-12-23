# Модели данных для блога:
# PublishedCreated: добавление поля для отметки о публикации и времени создания
# Category: категория публикации
# Location: местоположение публикаци
# Post: публикация с добавлением изображения, категории и местоположения
# Comment: комментарий для публикации


from django.db import models  # type: ignore[import-untyped]
from django.contrib.auth import get_user_model  # type: ignore[import-untyped]

# from .querysets import CustomQuerySet

User = get_user_model()


class PublishedCreated(models.Model):
    """
    Модель для добавления полей отметки о публикации и времени создания

    is_published - флаг Опубликовано.
    created_at - дата создания записи в БД.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(PublishedCreated):
    """
    Категория поста.

    title - название категории.
    description - описание категории.
    slug - слаг категории.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (
            f'{self.title[:30]} - {self.description[:30]} - {self.slug}'
        )


class Location(PublishedCreated):
    """
    Место, связанное с постом.

    name - название места.
    """

    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:30]


class Post(PublishedCreated):
    """
    Модель поста.

    title - название поста.
    text - текст поста.
    pub_date - дата публикации.
    author - автор поста.
    location - связанное место.
    category - категория поста.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно '
                   'делать отложенные публикации.'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts_for_author',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts_for_location',
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts_for_category',
        verbose_name='Категория',
    )
    image = models.ImageField('Изображение', upload_to='post_images',
                              blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', 'title')

    def __str__(self):
        return (
            f'{(self.author.get_username())[:30]} - {self.title[:30]} '
            f'{self.text[:50]} - {self.pub_date} '
            f'{self.location.name[:30]} - {self.category.title[:30]}'
        )


class Comment(models.Model):
    """
    Модель комментария для публикаций
    Атрибуты:
            text - текст комментария
            created_at - дата и время добавления комментария
            author - связь с пользователем, создавшим комментарий
            post - связь с публикацией, к которой относится комментарий
    """

    text = models.TextField('Текст')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        verbose_name='Публикация',
        related_name='comments'
    )

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'
        ordering = ('created_at',)
