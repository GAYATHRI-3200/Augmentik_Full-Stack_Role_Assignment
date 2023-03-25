from django.conf.global_settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail,EmailMessage
from .models import *

from django.conf import settings
from .forms import contactForm
from myproject import autoreply


from django.contrib.auth.models import User

def home(request):
    social_media_links = SocialMediaLink.objects.all()
    context = {'social_media_links': social_media_links}
    return render(request, 'home.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.info(request, 'Username or Password is Incorrect')

        return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for "+user)
                return redirect('login')

        context={'form': form}
        return render(request, 'register.html', context)


def contact(request):
    title = "Contact"
    form = contactForm(request.POST or None) #form handling by view.
    confirmation = None

    if form.is_valid():
        form.save()
        user_name = form.cleaned_data['Username']
        user_message = form.cleaned_data['Message']
        emailsub = user_name + " tried contacting you on SLD Prediction System."
        emailFrom = form.cleaned_data['UserEmail']
        emailmessage = 'user message:%s user name:%s user email: %s' %(user_message, user_name, emailFrom)
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(emailsub, emailmessage, emailFrom, list(emailTo), fail_silently=True)
        #Autoreply.
        autoreply.autoreply(emailFrom)
        title = "Thanks."
        confirmation = "We will get right back to you."
        form = None

    context = {'title':title, 'form':form, 'confirmation':confirmation,}
    template = 'contact.html'
    return render(request,'contact.html',context)