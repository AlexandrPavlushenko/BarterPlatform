from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from ads.models import Ad, ExchangeProposal

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["first_name"] = user.first_name or ""
        token["last_name"] = user.last_name or ""
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "city",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "phone": {"required": False},
            "avatar": {"required": False},
            "city": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "avatar", "city"]
        read_only_fields = ["id", "email"]


class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "author",
            "title",
            "description",
            "image",
            "category",
            "condition",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = UserSerializer(read_only=True)
    receiver_user = UserSerializer(read_only=True)
    ad = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = [
            "id",
            "ad_sender",
            "receiver_user",
            "ad",
            "comment",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "ad_sender",
            "receiver_user",
            "ad",
            "status",
            "created_at",
        ]


class ExchangeProposalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ["status"]
