from django.shortcuts import render
from user.forms import SignupForm, LoginForm,PasswordChangeForm,ProfileUpdateForm
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.contrib.auth import login as user_login,authenticate,logout as user_logout,update_session_auth_hash
from user.email import send_email_verification
from django.contrib.auth import get_user_model
from user.utils import EmailVerificationTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.decorators import login_required



User = get_user_model()
email_verification_token=EmailVerificationTokenGenerator()

# Create your views here.
def signup(request):
    form = SignupForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Please enter valid data')
            return render(request, 'user/signup.html', {'form': form})


    context={
        'form': form,
    }
    return render(request,'user/signup.html',context)


def login(request):
    form = LoginForm(request,data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,email=email, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request,'login successful')
                return HttpResponseRedirect(reverse('index'))

            messages.error(request, 'Please enter valid data')
            return HttpResponseRedirect(reverse('user:login'))
        messages.error(request, 'Please enter valid')
        return HttpResponseRedirect(reverse('user:login'))

    return render(request, 'user/login.html', {'form': form})

@login_required
def logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return HttpResponseRedirect(reverse('user:login'))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST,)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,"Password change successfully")
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Please enter valid data')
        return render(request,'user/change_password.html',{'form':form})

    context = {
        'form': PasswordChangeForm(request.user),
    }

    return render(request,'user/change_password.html',context)

@login_required
def profile_view(request):
    context={
        'user': request.user,
    }
    return render(request,'user/profile_view.html',context)

@login_required
def profile_update(request):

    if request.method == 'POST':
        form= ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
            return HttpResponseRedirect(reverse('user:profile'))
        messages.error(request, 'Please enter valid data')
        return render(request,'user/profile_update.html',{'form':form})


    context={
        'form':ProfileUpdateForm(instance=request.user),
    }
    return render(request,'user/profile_update.html',context)


@login_required
def email_verification_request(request):
    if not request.user.is_email_verified:
        send_email_verification(request,request.user.id)
        return HttpResponse('Email verification link sent to your email')
    return HttpResponseForbidden('Email already verified')

@login_required
def email_verifier(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None

    if user == request.user:
        if email_verification_token.check_token(user,token):
            user.is_email_verified=True
            user.save()
            messages.success(request,'Email is verified')
            return HttpResponseRedirect(reverse('user:profile'))
        return HttpResponseBadRequest('Invalid request')
    return HttpResponseForbidden('You dont have access to his user')
    
