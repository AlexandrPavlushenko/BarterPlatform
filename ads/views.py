from django.shortcuts import redirect
from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset


from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Ad
from .forms import AdForm

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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return redirect('ad_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.pk})

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return redirect('ad_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

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