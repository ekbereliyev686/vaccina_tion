from django.db import models
from campaign.models import Campaign,Slot
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class Vaccination(models.Model):
    patient=models.ForeignKey(User,related_name='patient',on_delete=models.CASCADE)
    campaign=models.ForeignKey(Campaign,on_delete=models.CASCADE)
    slot=models.ForeignKey(Slot,on_delete=models.CASCADE)
    date=models.DateField(null=True,blank=True)
    is_vaccinated=models.BooleanField(default=False)
    updated_date=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.get_full_name() + " | " + str(self.campaign.vaccine.name)

