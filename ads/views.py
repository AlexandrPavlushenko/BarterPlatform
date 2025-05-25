from django.shortcuts import redirect
from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm


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

        # Можно добавить другие данные, например:
        # context['related_ads'] = Ad.objects.filter(category=self.object.category).exclude(pk=self.object.pk)[:3]

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
        return reverse_lazy('ads:ad_list')

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = 'ads/proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_sender'] = get_object_or_404(Ad, pk=self.kwargs['ad_pk'], user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.ad_sender = get_object_or_404(Ad, pk=self.kwargs['ad_pk'], user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('proposal_list')

class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/proposal_list.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        )

class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = ExchangeProposal
    template_name = 'ads/proposal_detail.html'
    context_object_name = 'proposal'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.ad_sender.user != request.user and obj.ad_receiver.user != request.user:
            return redirect('proposal_list')
        return super().dispatch(request, *args, **kwargs)

class ProposalUpdateStatusView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = []
    template_name = 'ads/proposal_detail.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.ad_receiver.user != request.user:
            return redirect('proposal_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = kwargs.get('status')
        if status in ['accepted', 'rejected']:
            proposal = self.get_object()
            proposal.status = status
            proposal.save()
        return redirect('proposal_detail', pk=self.get_object().pk)