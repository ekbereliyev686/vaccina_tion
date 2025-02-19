from django.urls import path
from campaign import views

app_name = 'campaign'

urlpatterns = [
    path('',views.CampaignListView.as_view(),name='campaign-list'),
    path('<int:pk>',views.CampaignDetailView.as_view(),name='campaign-detail'),
    path('create',views.CampaignCreateView.as_view(),name='campaign-create'),
    path('update/<int:pk>',views.CampaignUpdateView.as_view(),name='campaign-update'),
    path('delete/<int:pk>',views.CampaignDeleteView.as_view(),name='campaign-delete'),
    path('<int:campaign_id>/slot/',views.SlotListView.as_view(),name='slot_list'),
    path('slot/<int:pk>',views.SlotDetailView.as_view(),name='slot-detail'),
    path('<int:campaign_id>/slot/create',views.SlotCreate.as_view(), name='slot-create'),
    path('campaign/<int:campaign_id>/slot/update/<int:pk>/',views.SlotUpdate.as_view(), name='slot-update'),
    path('slot/delete/<int:pk>/',views.SlotDelete.as_view(), name='slot-delete'),
   
]

# <int:campaign_id>