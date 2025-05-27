from django.conf import settings
from django.db import models


class Ad(models.Model):
    """Модель объявления для системы обмена товарами.

    Attributes:
        CONDITION_CHOICES (list): Варианты состояния товара
        CATEGORY_CHOICES (list): Доступные категории товаров

    Fields:
        author (ForeignKey): Ссылка на пользователя-автора
        title (CharField): Заголовок объявления (макс. 100 символов)
        description (TextField): Описание товара (макс. 500 символов)
        image (ImageField): Фото товара (необязательное)
        category (CharField): Категория товара из CATEGORY_CHOICES
        condition (CharField): Состояние товара из CONDITION_CHOICES
        created_at (DateTimeField): Дата создания (автоматически)
        updated_at (DateTimeField): Дата обновления (автоматически)
    """

    CONDITION_CHOICES = [
        ("new", "Новое"),
        ("used", "Б/у"),
    ]

    CATEGORY_CHOICES = [
        ("electronics", "Электроника"),
        ("clothing", "Одежда"),
        ("books", "Книги"),  # Добавить категории при необходимости #
        ("furniture", "Мебель"),
        ("other", "Другое"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    image = models.ImageField(
        upload_to="ads/images/", null=True, blank=True, verbose_name="Фото"
    )
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория"
    )
    condition = models.CharField(
        max_length=50, choices=CONDITION_CHOICES, verbose_name="Состояние"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        """Строковое представление объявления (используется в админке)."""
        return self.title

    class Meta:
        """Мета-класс для дополнительных настроек модели.

        Attributes:
            verbose_name: Имя модели
            verbose_name_plural: Имя во множественном числе
            ordering: Сортировка по умолчанию (новые сначала)
        """

        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class ExchangeProposal(models.Model):
    """Модель предложения обмена между пользователями.

    Attributes:
        STATUS_CHOICES (list): Возможные статусы предложения

    Fields:
        ad_sender (ForeignKey): Пользователь, отправивший предложение
        receiver_user (ForeignKey): Автор объявления (получатель)
        ad (ForeignKey): Связанное объявление
        comment (TextField): Комментарий к предложению (макс. 500 символов)
        status (CharField): Статус предложения из STATUS_CHOICES
        created_at (DateTimeField): Дата создания (автоматически)
    """

    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принята"),
        ("rejected", "Отклонена"),
    ]

    # Отправитель предложения
    ad_sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_proposals",
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
    )

    # Автор объявления (получатель предложения)
    receiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_proposals",
        on_delete=models.CASCADE,
        verbose_name="Получатель",
        null=True,
        blank=True,
    )

    # Связанное объявление
    ad = models.ForeignKey(
        Ad,
        related_name="exchange_proposals",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Объявление",
    )

    comment = models.TextField(max_length=500, verbose_name="Комментарий")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        """Строковое представление предложения обмена."""
        return f"Предложение от {self.ad_sender} к {self.receiver_user} для объявления '{self.ad.title}'"

    class Meta:
        """Мета-класс для дополнительных настроек модели.

        Attributes:
            unique_together: Ограничение на уникальность (1 предложение от пользователя на объявление)
            verbose_name: Имя модели
            verbose_name_plural: Имя во множественном числе
            ordering: Сортировка по умолчанию (новые сначала)
        """

        unique_together = [
            "ad_sender",
            "ad",
        ]  # Один пользователь - одно предложение на объявление
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ["-created_at"]
