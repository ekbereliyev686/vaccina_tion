from django.contrib import admin
from .models import Vaccination
# Register your models here.

@admin.register(Vaccination)
class CustomVaccination(admin.ModelAdmin):
    list_display = ['patient','campaign','slot','is_vaccinated',]
    search_fields = ['patient__first_name','patient_last_name']
    list_filter = ['is_vaccinated']
    readonly_fields = ['patient','campaign','is_vaccinated','updated_date','date']
    change_form_template = 'admin/change_vaccination.html'


# admin.site.register(Vaccination, CustomVaccination)