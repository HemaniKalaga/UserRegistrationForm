from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse
from django.core.mail import send_mail
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
            MUFDO.set_password(pw)
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

#licy xtuu wvnl lifo