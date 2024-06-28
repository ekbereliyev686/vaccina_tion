from django.contrib import admin
from .models import Campaign,Slot


class SlotInline(admin.TabularInline):
    model = Slot
    readonly_fields = ['reserved']

class CustomCampaign(admin.ModelAdmin):
    inlines = [SlotInline]
    search_fields = ['center__name','vaccine__name']
    list_display = ['vaccine','center','start_date','end_date']
    odering = ['-start_date']
    fields = (('vaccine'),('center'),('start_date','end_date'))


admin.site.register(Campaign, CustomCampaign)
