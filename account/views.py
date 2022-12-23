from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import Customer
from .forms import SignUpForm, GenderForm, CustomerUpdateForm

# Create your views here.
def sign_in(request):
    valuenext = request.POST.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:                                                
            login(request, user)         
            if valuenext != '':
                return redirect(valuenext)            
            else:
                return redirect('store:home')               
        else:
            messages.info(request, 'username or password is incorrect')
            
    return render(request, 'accounts/sign-in.html')

def sign_up(request):
    gender_form = GenderForm()
    sign_up_form = SignUpForm()
    
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)  
        gender_form = GenderForm(request.POST)  
        if sign_up_form.is_valid() and gender_form.is_valid():
            user_account = sign_up_form.save()      
            customer_gender = gender_form['gender'].value()
            Customer.objects.create(user=user_account, gender=customer_gender)
            messages.success(request, 'Sign up successfully')
            return redirect('account:sign-in')

    context = {'sign_up_form': sign_up_form, 'gender_form': gender_form}
    return render(request, 'accounts/sign-up.html', context)

def profile(request):
    customer_update_form = CustomerUpdateForm(instance=request.user)
    gender_form = GenderForm(instance=request.user.customer)

    if request.method == 'POST':
        customer_update_form = CustomerUpdateForm(request.POST, instance=request.user)
        gender_form = GenderForm(request.POST, instance=request.user)        
        if customer_update_form.is_valid() and gender_form.is_valid():
            first_name = customer_update_form.cleaned_data.get('first_name')
            messages.success(request, f'{first_name}, your account has been updated!')                    
            customer_update_form.save()
            gender_form.save()
            return redirect('account:profile')

    context = {'gender_form': gender_form, 'customer_update_form': customer_update_form}
    return render(request, 'accounts/profile.html', context)

def sign_out(request):
    logout(request)
    return redirect('store:home')

def delete_user(request):
    User.objects.get(username=request.user).delete()
    messages.success(request, 'your account has been deleted')                    
    return redirect('store:home')
