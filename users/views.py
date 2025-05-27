from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import UserProfileForm, UserRegisterForm
from .models import User


class CustomAuthenticationForm(AuthenticationForm):
    """Кастомная форма аутентификации с email вместо username.

    Attributes:
        error_messages (dict): Словарь сообщений об ошибках:
            - invalid_login: Неверные учетные данные
            - inactive: Аккаунт деактивирован
            - missing_fields: Не заполнены обязательные поля
    """

    error_messages = {
        "invalid_login": _("Неверная почта или пароль."),
        "inactive": _("Ваш аккаунт деактивирован. Обратитесь к администратору."),
        "missing_fields": _("Пожалуйста, заполните оба поля."),
    }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с измененными labels полей."""
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Пароль"

    def clean(self):
        """Валидация формы аутентификации.

        Returns:
            dict: Очищенные данные формы

        Raises:
            forms.ValidationError: Если:
                - не заполнены обязательные поля
                - пользователь неактивен
                - неверные учетные данные
        """
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError(
                self.error_messages["missing_fields"],
                code="missing_fields",
            )

        if email and password:
            try:
                user = User.objects.get(email=email)

                if not user.is_active:
                    raise forms.ValidationError(
                        self.error_messages["inactive"],
                        code="inactive",
                    )

                self.user_cache = authenticate(
                    self.request, email=email, password=password
                )

                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages["invalid_login"],
                        code="invalid_login",
                    )

            except User.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )

        return self.cleaned_data


class CustomLoginView(LoginView):
    """Кастомное представление для входа пользователя.

    Attributes:
        form_class (Form): Класс формы аутентификации
        template_name (str): Путь к шаблону страницы входа
    """

    form_class = CustomAuthenticationForm
    template_name = "users/login.html"

    def form_invalid(self, form):
        """Обработка невалидной формы входа.

        Args:
            form (Form): Невалидная форма

        Returns:
            HttpResponse: Ответ с ошибками валидации
        """
        storage = messages.get_messages(self.request)
        storage.used = False

        for error in form.errors.get("__all__", []):
            messages.error(self.request, str(error))

        return super().form_invalid(form)


class UserCreateView(generic.CreateView):
    """Представление для регистрации нового пользователя.

    Attributes:
        model (Model): Модель пользователя
        template_name (str): Путь к шаблону
        success_url (str): URL для перенаправления после успешной регистрации
        form_class (Form): Класс формы регистрации
    """

    model = User
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")
    form_class = UserRegisterForm

    def form_valid(self, form):
        """Обработка валидной формы регистрации.

        Args:
            form (Form): Валидная форма регистрации

        Returns:
            HttpResponseRedirect: Перенаправление на страницу входа
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        self.send_confirmation_email(user, token)

        messages.success(
            self.request,
            "Регистрация прошла успешно! Пожалуйста,"
            " проверьте свою электронную почту для активации учетной записи.",
        )
        return HttpResponseRedirect(self.success_url)

    def send_confirmation_email(self, user, token):
        """Отправка письма с подтверждением регистрации.

        Args:
            user (User): Объект пользователя
            token (str): Токен активации
        """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = "Активируйте свой аккаунт"
        activation_link = (
            f"http://{current_site.domain}"
            f"{reverse('users:activate', kwargs={'uidb64': uid, 'token': token})}"
        )

        message = render_to_string(
            "users/activation_email.html",
            {
                "user": user,
                "activation_link": activation_link,
            },
        )
        email = EmailMultiAlternatives(mail_subject, message, to=[user.email])
        email.send()


class ActivateView(generic.View):
    """Представление для активации учетной записи пользователя."""

    def get(self, request, uidb64, token):
        """Активация учетной записи по ссылке из email.

        Args:
            uidb64 (str): Закодированный ID пользователя
            token (str): Токен активации

        Returns:
            HttpResponse: Страница успешной активации или ошибки
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, "users/activation_complete.html")
            return render(request, "users/activation_invalid.html")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, "users/activation_invalid.html")


class UserProfileUpdateView(generic.UpdateView):
    """Представление для обновления профиля пользователя.

    Attributes:
        model (Model): Модель пользователя
        form_class (Form): Форма редактирования профиля
        template_name (str): Шаблон страницы профиля
        success_url (str): URL для перенаправления после успешного обновления
    """

    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("main:index")

    def get_object(self, queryset=None):
        """Получение текущего пользователя.

        Returns:
            User: Текущий аутентифицированный пользователь
        """
        return self.request.user

    def form_valid(self, form):
        """Обработка валидной формы профиля.

        Args:
            form (Form): Валидная форма профиля

        Returns:
            HttpResponse: Результат родительского метода
        """
        if self.request.POST.get("remove_avatar"):
            self.object.avatar.delete(save=False)
            self.object.avatar = None

        form.instance.is_published = "is_published" in self.request.POST
        return super().form_valid(form)


class PasswordResetRequestView(generic.View):
    """Представление для запроса сброса пароля."""

    def get(self, request):
        """Отображение формы запроса сброса пароля.

        Returns:
            HttpResponse: Страница запроса сброса пароля
        """
        return render(request, "users/password_reset.html")

    def post(self, request):
        """Обработка запроса на сброс пароля.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу входа
            HttpResponse: Страница запроса с ошибкой, если email не найден
        """
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Пользователь с этой почтой не найден.")
            return render(request, "users/password_reset.html")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = (
            f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
        )

        subject = "Сброс пароля"
        message = render_to_string(
            "users/password_reset_email.html",
            {"user": user, "activation_link": activation_link},
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        messages.success(request, "Ссылка на сброс пароля отправлена на вашу почту.")
        return redirect("users:login")


class PasswordResetConfirmView(generic.View):
    """Представление для подтверждения сброса пароля."""

    def get(self, request, uidb64, token):
        """Отображение формы ввода нового пароля.

        Args:
            uidb64 (str): Закодированный ID пользователя
            token (str): Токен сброса пароля

        Returns:
            HttpResponse: Страница ввода нового пароля
        """
        return render(
            request,
            "users/password_reset_confirm.html",
            {"uidb64": uidb64, "token": token},
        )

    def post(self, request, uidb64, token):
        """Обработка формы сброса пароля.

        Args:
            uidb64 (str): Закодированный ID пользователя
            token (str): Токен сброса пароля

        Returns:
            HttpResponseRedirect: Перенаправление при успешном сбросе
            HttpResponse: Форма с ошибками при неудаче
        """
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 or not password2:
            messages.error(request, "Пожалуйста, введите оба пароля.")
            return render(
                request,
                "users/password_reset_confirm.html",
                {"uidb64": uidb64, "token": token},
            )

        if password1 != password2:
            messages.error(
                request, "Пароли не совпадают. Пожалуйста, попробуйте еще раз."
            )
            return render(
                request,
                "users/password_reset_confirm.html",
                {"uidb64": uidb64, "token": token},
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(password1)
                user.save()
                messages.success(request, "Ваш пароль был успешно сброшен.")
                return redirect("users:password_reset_complete")

            messages.error(request, "Ссылка сброса пароля недействительна.")
            return render(
                request,
                "users/password_reset_confirm.html",
                {"uidb64": uidb64, "token": token},
            )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Недействительная ссылка сброса пароля.")
            return render(
                request,
                "users/password_reset_confirm.html",
                {"uidb64": uidb64, "token": token},
            )


class PasswordResetCompleteView(generic.View):
    """Представление страницы успешного сброса пароля."""

    def get(self, request):
        """Отображение страницы успешного сброса пароля.

        Returns:
            HttpResponse: Страница подтверждения сброса пароля
        """
        return render(request, "users/password_reset_complete.html")
