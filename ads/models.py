from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
    ]

    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('furniture', 'Мебель'),
        ('other', 'Другое'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    image = models.ImageField(upload_to='ads/images/', null=True, blank=True, verbose_name="Фото")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, verbose_name="Состояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    # Отправитель предложения
    ad_sender = models.ForeignKey(
        User,
        related_name='sent_proposals',
        on_delete=models.CASCADE,
        verbose_name="Отправитель"
    )

    # Автор объявления (получатель предложения)
    receiver_user = models.ForeignKey(
        User,
        related_name='received_proposals',
        on_delete=models.CASCADE,
        verbose_name="Получатель",
        null=True,
        blank=True
    )

    # Связанное объявление
    ad = models.ForeignKey(
        Ad,
        related_name='exchange_proposals',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Объявление"
    )

    comment = models.TextField(max_length=500, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Предложение от {self.ad_sender} к {self.receiver_user} для объявления '{self.ad.title}'"

    class Meta:
        unique_together = ['ad_sender', 'ad']  # Один пользователь - одно предложение на объявление
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ['-created_at']
