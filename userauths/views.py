from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout , update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import User , Account , KYC
from .forms import UserRegisterForm  , UserPasswordChangeForm , UserKYCForm


# Create your views here.



def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("userauths:account")
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']  
            new_user.save()
            
            messages.success(request, f'Account created for {new_user.username}! You are now able to log in.')
            
            new_user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            
            if new_user is not None:
                login(request, new_user)
                return redirect("userauths:account")
            else:
                messages.error(request, "Authentication failed. Please log in manually.")
                return redirect("userauths:login")
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None: # if there is a user
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect("userauths:account")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect("userauths:account")

    return render(request, 'userauths/sign-in.html')




