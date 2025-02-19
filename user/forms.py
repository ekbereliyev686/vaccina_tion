from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from center import forms

User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self,*args, **kwargs):
        super(SignupForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class']='form-control'
    class Meta:
        model = User
        fields =['email','first_name','last_name','date_of_birth','gender','photo','identity_document_type','identity_document_number']


class LoginForm(AuthenticationForm):

    def __init__(self,*args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():

































































            visible.field.widget.attrs['class']='form-control'

    class Meta:
        model = User
        fields = ['email','password']


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self,*args, **kwargs):
        super(ChangePasswordForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class']='form-control'

    class Meta:
        model = User
        fields ='__all__'



class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields=[
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'photo',
            'identity_document_type',
            'identity_document_number',
        ]