from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse, reverse_lazy
from .forms import AccountForm, CreateUserForm, EditProfileForm

 # New
from .models import Account, Posts
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required(login_url='signin')
def home(request):
    return render(request, 'account/main.html')


# Authentication Views
def signup(request):

        form = CreateUserForm()
        account_form = AccountForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            account_form = AccountForm(request.POST)
            if form.is_valid() and account_form.is_valid():
                    user = form.save()
                    account = account_form.save(commit=False)
                    account.user = user
                    account.save()
                    username = form.cleaned_data.get('username')


                    messages.success(request, 'Account was created for ' + username)

                    return redirect('account:signin')

        context = {'form': form, 'account_form': account_form} 
        return render(request, 'account/signup.html', context)



def signin(request):
    #New - from video
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.get(username=username)
        account = Account.objects.get(user=user)
        if account is not None:
            userAuth = authenticate(request, username=username, password=password)  
            if userAuth is not None:
                is_teacher = account.is_teacher
                login(request, user)
                if is_teacher:
                    return redirect('teachers:main')
                else:
                    return redirect('students:main')
            else:
                messages.info(request, 'Username OR Password is incorrect')    

    
    context = {}
    return render(request, 'account/signin.html')

@login_required
def signout(request):
    logout(request)
    url = reverse('account:signin')

    return redirect('account:signin')
