from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import Customer
from .forms import SignUpForm, CustomerForm

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
    customer_form = CustomerForm()
    sign_up_form = SignUpForm()
    
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)  
        customer_form = CustomerForm(request.POST)  
        if sign_up_form.is_valid() and customer_form.is_valid():
            user_account = sign_up_form.save()      
            customer_gender = customer_form['gender'].value()
            Customer.objects.create(user=user_account, gender=customer_gender)
            messages.success(request, 'Sign up successfully')
            return redirect('account:sign-in')

    context = {'sign_up_form': sign_up_form, 'customer_form': customer_form}
    return render(request, 'accounts/sign-up.html', context)

def sign_out(request):
    logout(request)
    return redirect('store:home')