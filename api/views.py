from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from ads.models import Ad, ExchangeProposal

from .paginators import StandardResultsSetPagination
from .permissions import IsOwnerOnly
from .serializers import (AdSerializer, CustomTokenObtainPairSerializer,
                          ExchangeProposalSerializer,
                          ExchangeProposalUpdateSerializer,
                          UserRegisterSerializer)

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """Кастомное представление для получения JWT токенов.

    Использует CustomTokenObtainPairSerializer для добавления
    дополнительных полей пользователя в токен.
    """

    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """Представление для регистрации новых пользователей.

    Разрешает доступ без аутентификации.
    Использует UserRegisterSerializer для валидации данных.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class AdListView(generics.ListAPIView):
    """Представление для получения списка объявлений с фильтрацией.

    Поддерживает:
    - Пагинацию (StandardResultsSetPagination)
    - Фильтрацию по параметрам:
      * my_ads - показывать только свои объявления
      * search - поиск по заголовку и описанию
      * category - фильтр по категории
      * condition - фильтр по состоянию
    """

    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Ad.objects.all()

        show_my_ads = self.request.query_params.get("my_ads", "").lower() == "true"
        search_query = self.request.query_params.get("search", None)
        category = self.request.query_params.get("category", None)
        condition = self.request.query_params.get("condition", None)

        if show_my_ads and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        elif self.request.user.is_authenticated:
            queryset = queryset.exclude(author=self.request.user)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.order_by("-created_at")


class AdDetailView(generics.RetrieveAPIView):
    """Представление для просмотра деталей объявления."""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdCreateView(generics.CreateAPIView):
    """Представление для создания нового объявления.

    Автоматически устанавливает текущего пользователя как автора.
    Требует аутентификации.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdUpdateView(generics.UpdateAPIView):
    """Представление для обновления объявления.

    Разрешает редактирование только владельцу объявления.
    Использует permission IsOwnerOnly.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Ad, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class AdDeleteView(generics.DestroyAPIView):
    """Представление для удаления объявления.

    Разрешает удаление только владельцу объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ExchangeProposalListView(generics.ListAPIView):
    """Представление для получения списка предложений обмена.

    Показывает предложения, где пользователь:
    - Является отправителем ИЛИ
    - Является получателем
    """

    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender=self.request.user) | Q(receiver_user=self.request.user)
        ).order_by("-created_at")


class ExchangeProposalDetailView(generics.RetrieveAPIView):
    """Представление для просмотра деталей предложения обмена.

    Доступно только для участников предложения (отправитель/получатель).
    """

    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender=self.request.user) | Q(receiver_user=self.request.user)
        )


class ExchangeProposalCreateView(generics.CreateAPIView):
    """Представление для создания предложения обмена.

    Проверяет:
    - Пользователь не автор объявления
    - Предложение еще не отправлялось
    Автоматически устанавливает:
    - Отправителя (текущий пользователь)
    - Получателя (автор объявления)
    - Объявление
    """

    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad_id = self.request.data.get("ad")
        ad = get_object_or_404(Ad, pk=ad_id)

        if ad.author == self.request.user:
            raise serializers.ValidationError(
                "Вы не можете отправить предложение на свое собственное объявление."
            )

        if ExchangeProposal.objects.filter(ad_sender=self.request.user, ad=ad).exists():
            raise serializers.ValidationError(
                "Вы уже отправили предложение по этому объявлению."
            )

        serializer.save(ad_sender=self.request.user, receiver_user=ad.author, ad=ad)


class ExchangeProposalUpdateView(generics.UpdateAPIView):
    """Представление для обновления статуса предложения.

    Доступно только получателю предложения.
    При принятии предложения (status="accepted"):
    - Все остальные предложения по этому объявлению автоматически отклоняются
    """

    serializer_class = ExchangeProposalUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(receiver_user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()

        if serializer.validated_data.get("status") == "accepted":
            ExchangeProposal.objects.filter(ad=instance.ad).exclude(
                pk=instance.pk
            ).update(status="rejected")

        serializer.save()


class ExchangeProposalDeleteView(generics.DestroyAPIView):
    """Представление для удаления предложения обмена.

    Разрешает удаление только отправителю предложения.
    """

    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender=self.request.user)
