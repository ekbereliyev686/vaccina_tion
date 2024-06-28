from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from campaign.models import Campaign, Slot
from vaccination.models import Vaccination
from campaign.forms import CampaignForm,SlotForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class CampaignListView(LoginRequiredMixin,generic.ListView):
    model = Campaign
    template_name = 'campaign/campaign_list.html'
    paginate_by = 2
    ordering = ['-id']

class CampaignDetailView(LoginRequiredMixin,generic.DetailView):
    model = Campaign
    template_name = 'campaign/campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context ['registiration'] = Vaccination.objects.filter(campaign=self.kwargs['pk']).count()
        context['registiration'] = 5

        return context


class CampaignCreateView(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaign/campaign_create.html'
    permission_required = ('campaign.add_campaign',)
    success_message = "Campaign created successfully"
    success_url = reverse_lazy('campaign:campaign-list')


class CampaignUpdateView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ('campaign.change_campaign',)
    template_name = 'campaign/campaign_update.html'
    success_message = "Campaign updated successfully"
    success_url = reverse_lazy('campaign:campaign-list')


class CampaignDeleteView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,generic.DeleteView):
    model = Campaign
    permission_required = ('campaign.delete_campaign',)
    template_name = 'campaign/campaign_delete.html'
    success_message = 'Campaign deleted successfully'
    success_url = reverse_lazy('campaign:campaign-list')

class SlotListView(LoginRequiredMixin,generic.ListView):
    model = Slot
    template_name = 'campaign/slot_list.html'
    paginate_by = 2

    def get_queryset(self):
        queryset= Slot.objects.filter(campaign=self.kwargs['campaign_id']).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context ['campaign_id'] =self.kwargs['campaign_id']
        return context
class SlotDetailView(LoginRequiredMixin,generic.DetailView):
    model = Slot
    template_name = 'campaign/slot_detail.html'


class SlotCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,generic.CreateView):
    model = Slot
    form_class = SlotForm
    template_name = 'campaign/slot_create.html'
    success_message = "Slot created successfully"
    permission_required = ('campaign.add_slot',)

    def get_success_url(self):
        return reverse_lazy('campaign:slot_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_initial(self):
        initial= super().get_initial()
        initial['campaign'] = Campaign.objects.get(id=self.kwargs['campaign_id'])
        return initial


    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs() 
        kwargs['campaign_id'] = self.kwargs['campaign_id']
        return kwargs


class SlotUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,generic.UpdateView):
    model = Slot
    form_class = SlotForm
    template_name = 'campaign/slot_update.html'
    permission_required = ('campaign.change_slot',)
    success_message = "Slot updated successfully"

    def get_success_url(self):
        return reverse_lazy('campaign:slot_list', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_initial(self):
        initial = super().get_initial()
        initial['campaign'] = Campaign.objects.get(id=self.kwargs['campaign_id'])
        return initial

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs() 
        kwargs['campaign_id'] = self.kwargs['campaign_id']
        return kwargs


class SlotDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,generic.DeleteView):
    model = Slot
    template_name = 'campaign/slot_delete.html'
    permission_required = ('campaign.delete_slot',)
    success_message = "Slot delete successfully"

    def get_success_url(self):
        return reverse_lazy('campaign:slot_list', kwargs={'campaign_id': self.get_object().campaign_id})
