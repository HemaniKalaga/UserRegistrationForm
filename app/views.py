from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
  
    if request.method=='POST' and request.FILES:
        ufo=UserForm(request.POST)
        pfo=ProfileForm(request.POST,request.FILES)
        if ufo.is_valid() and pfo.is_valid():
            MUFDO=ufo.save(commit=False)
            pw=ufo.cleaned_data['password']
            e=ufo.cleaned_data['email']
            MUFDO.set_password(pw)
            MUFDO.set_password(e)
            MUFDO.save()

            MPFDO=pfo.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Registration',
                      'Congratulations! Your registration is successfull...Hurray!',
                      'kalagahemani1234@gmail.com',
                      [MUFDO.email],
                      fail_silently=False)
            
            return HttpResponse('Registration is Successfull')
        else:
            return HttpResponse('Invalid')

    return render(request,'registration.html',d)

def home_page(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home_page.html',d)
    return render(request,'home_page.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home_page'))
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


