from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 8
    form_class = AdForm

    def get_queryset(self):
        queryset = super().get_queryset()

        # Определяем, нужно ли показывать только объявления пользователя
        show_my_ads = self.request.GET.get('my_ads') == 'true' and self.request.user.is_authenticated

        if show_my_ads:
            # Показываем только объявления текущего пользователя
            queryset = queryset.filter(author=self.request.user)
        else:
            # В обычном режиме исключаем объявления текущего пользователя
            if self.request.user.is_authenticated:
                queryset = queryset.exclude(author=self.request.user)

        # Поиск по ключевым словам
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Фильтрация по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Фильтрация по состоянию
        condition = self.request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_condition'] = self.request.GET.get('condition', '')
        context['Ad'] = Ad
        context['show_my_ads'] = self.request.GET.get('my_ads') == 'true'
        return context


class AdDetailView(DetailView):
    """
    Класс для отображения детальной страницы объявления.
    Наследуется от Django's DetailView.
    """
    model = Ad  # Указываем модель, с которой работаем
    template_name = 'ads/ad_detail.html'  # Путь к шаблону
    context_object_name = 'ad'  # Имя переменной в шаблоне

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительные данные в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)

        # Добавляем текущего пользователя в контекст
        context['user'] = self.request.user

        # Обновляем фильтрацию - используем поле ad вместо ad_receiver
        if self.request.user.is_authenticated:
            context['exchange_proposals'] = ExchangeProposal.objects.filter(
                ad=self.object,  # Используем ad вместо ad_receiver
                ad_sender=self.request.user
            )

            # Если пользователь - автор объявления, показываем все полученные предложения
            if self.request.user == self.object.author:
                context['received_proposals'] = ExchangeProposal.objects.filter(
                    ad=self.object
                ).exclude(ad_sender=self.request.user)
        else:
            context['exchange_proposals'] = ExchangeProposal.objects.none()

        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def get_success_url(self):
        return reverse_lazy('ads:ad_detail', kwargs={'pk': self.object.pk})


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/ad_detail.html'

    def get_success_url(self):
        return reverse_lazy('ads:ad_detail', kwargs={'pk': self.kwargs['ad_id']})

    def form_valid(self, form):
        ad = get_object_or_404(Ad, pk=self.kwargs['ad_id'])



        # Проверяем, не отправлял ли уже пользователь предложение (теперь проверяем по полю ad)
        if ExchangeProposal.objects.filter(ad_sender=self.request.user, ad=ad).exists():
            messages.error(self.request, "Вы уже отправляли предложение обмена для этого объявления.")
            return super().form_invalid(form)

        # Сохраняем предложение
        proposal = form.save(commit=False)
        proposal.ad_sender = self.request.user
        proposal.receiver_user = ad.author  # Автор объявления
        proposal.ad = ad  # Само объявление
        proposal.save()
        print(proposal.ad_sender, proposal.receiver_user)
        messages.success(self.request, "Ваше предложение обмена успешно отправлено!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = get_object_or_404(Ad, pk=self.kwargs['ad_id'])
        context['ad'] = ad

        # Обновляем фильтрацию по полю ad вместо ad_receiver
        context['exchange_proposals'] = ExchangeProposal.objects.filter(
            ad=ad,
            ad_sender=self.request.user
        )

        # Если пользователь - автор объявления, показываем все предложения к этому объявлению
        if self.request.user == ad.author:
            context['received_proposals'] = ExchangeProposal.objects.filter(
                ad=ad
            ).exclude(ad_sender=self.request.user)

        return context

