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




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('userauths:sign-in')



@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None
    
    if request.method == "POST":
        form = UserKYCForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.save()
            
            kyc, created = KYC.objects.get_or_create(user=user)
            kyc.image = form.cleaned_data.get('image', kyc.image)
            kyc.save()

            messages.success(request, "The data has been updated successfully.")
            return redirect("core:home")
    else:
        form = UserKYCForm(instance=user)
    
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "userauths/kyc-form.html", context)




@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            # messages.warning(request, "You need to submit your kyc")
            return redirect("userauths:kyc-registration")
            return redirect("core:home")
        
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "userauths/account.html", context)




@login_required
def delete_account(request):
    user = request.user
    if request.method == "POST":
        Account.objects.filter(user=user).delete()
        KYC.objects.filter(user=user).delete()

        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("userauths:sign-in")

    return render(request, "userauths/delete_account.html")



@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('userauths:account')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPasswordChangeForm(request.user)

    return render(request, 'userauths/change_password.html', {'form': form})