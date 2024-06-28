from django.shortcuts import render,get_object_or_404
from django.views import View
from vaccin.models import Vaccine
from vaccin.forms import VaccineForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class VaccineList(View):
    queryset = Vaccine.objects.all()
    template_name = 'vaccine/vaccine_list.html'
    ordering=['-id']
    paginate_by=2
    def get(self,request):
        vaccine_list=Vaccine.objects.all()
        context={
            'vaccine_list':vaccine_list
        }

        return render(request,'vaccine/vaccine_list.html',context)


@method_decorator(login_required, name='dispatch')
class Vaccinedetail(View):
    def get(self,request,pk):
        vaccine_detail=Vaccine.objects.get(pk=pk)
        context={
            'vaccine_detail':vaccine_detail
        }
        return render(request,'vaccine/vaccine_detail.html',context)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.add_vaccine',raise_exception=True), name='dispatch')
class VaccineCreate(View):
    form_class=VaccineForm
    template_name='vaccine/create_vaccine.html'


    def get(self,request):
        context={
            'form':self.form_class
        }
        return render(request,self.template_name,context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vaccin:list'))
        return render(request, self.template_name,{'form':form})

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.change_vaccine',raise_exception=True), name='dispatch')
class VaccineUpdate(View):
    form_class=VaccineForm
    template_name='vaccine/update_vaccine.html'

    def get(self,request,pk):
        vaccine=get_object_or_404(Vaccine,pk=pk)
        context={
                'form':self.form_class(instance=vaccine)
                }
        return render(request,self.template_name,context)


    def post(self,request,pk):
        vaccine=Vaccine.objects.get(pk=pk)
        form=self.form_class(request.POST,instance=vaccine)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vaccin:detail',kwargs={'pk':vaccine.pk}))
        return render(request,self.template_name,{'form':form})
#    

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.delete_vaccine',raise_exception=True), name='dispatch')
class VaccineDelete(View):  
    template_name='vaccine/delete_vaccine.html'
    
    def get(self,request,pk):
        vaccine=get_object_or_404(Vaccine,pk=pk)
        context={
                'vaccine':vaccine
            }
        return render(request,self.template_name,context)


    def post(self,request,pk):
        Vaccine.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('vaccin:list'))