from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .permissions import IsOwnerOnly

from ads.models import Ad, ExchangeProposal
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterSerializer,
    AdSerializer,
    ExchangeProposalSerializer,
    ExchangeProposalUpdateSerializer,
)
from .paginators import StandardResultsSetPagination

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class AdListView(generics.ListAPIView):
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
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdUpdateView(generics.UpdateAPIView):
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
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ExchangeProposalListView(generics.ListAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Показываем предложения, где пользователь либо отправитель, либо получатель
        return ExchangeProposal.objects.filter(
            Q(ad_sender=self.request.user) | Q(receiver_user=self.request.user)
        ).order_by("-created_at")


class ExchangeProposalDetailView(generics.RetrieveAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем предложения, где пользователь либо отправитель, либо получатель
        return ExchangeProposal.objects.filter(
            Q(ad_sender=self.request.user) | Q(receiver_user=self.request.user)
        )


class ExchangeProposalCreateView(generics.CreateAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad_id = self.request.data.get("ad")
        ad = get_object_or_404(Ad, pk=ad_id)

        # Проверяем, что пользователь не автор объявления
        if ad.author == self.request.user:
            raise serializers.ValidationError(
                "Вы не можете отправить предложение на свое собственное объявление."
            )

            # Проверяем, что предложение еще не отправлялось
        if ExchangeProposal.objects.filter(ad_sender=self.request.user, ad=ad).exists():
            raise serializers.ValidationError(
                "Вы уже отправили предложение по этому объявлению."
            )

        serializer.save(ad_sender=self.request.user, receiver_user=ad.author, ad=ad)


class ExchangeProposalUpdateView(generics.UpdateAPIView):
    serializer_class = ExchangeProposalUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Только получатель предложения может обновлять статус
        return ExchangeProposal.objects.filter(receiver_user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()

        # Если статус меняется на "accepted", отклоняем все остальные предложения
        if serializer.validated_data.get("status") == "accepted":
            ExchangeProposal.objects.filter(ad=instance.ad).exclude(
                pk=instance.pk
            ).update(status="rejected")

        serializer.save()


class ExchangeProposalDeleteView(generics.DestroyAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Удалять можно только свои предложения
        return ExchangeProposal.objects.filter(ad_sender=self.request.user)
