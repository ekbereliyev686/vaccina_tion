from django.db import models
from center.models import Center
from vaccin.models import Vaccine
from django.contrib.auth import get_user_model

User = get_user_model()

class Campaign(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    agents = models.ManyToManyField(User)

def __str__(self):
    return self.center.name + " - " + self.vaccine.name



class Slot(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    max_capacity = models.IntegerField(default=0,null=True,blank=True)
    reserved=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.date) + " | " + str(self.start_time) + " to " + str(self.end_time)

    def reverse_vaccine(campaign_id,slot_id):
        from center.models import Storage
        from django.db.models import F

        slot = Slot.objects.get(pk=slot_id)
        campaign = Campaign.objects.get(pk=campaign_id)
        storage = Storage.objects.get(center=campaign.center,vaccine=campaign.vaccine)

        if(storage.total_quantity) > 0 and (storage.booked_quantity) < (storage.total_quantity) and (slot.max_capacity> slot.reserved) :
            slot.reserved =F('reserved') + 1
            storage.booked_quantity =F('booked_quantity') + 1
            slot.save()
            storage.save()
            return True
        return False
