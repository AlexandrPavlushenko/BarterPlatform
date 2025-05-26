from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from ads.models import Ad, ExchangeProposal

from .paginators import AdListPagination, ExchangeProposalPaginator
from .serializers import AdSerializer, ExchangeProposalPaginator, MyTokenObtainPairSerializer, UserRegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """Представление для получения токенов доступа и обновления на основе пользовательских учетных данных."""

    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """Представление для регистрации нового пользователя."""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
