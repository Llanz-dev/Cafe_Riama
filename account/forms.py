from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from django import forms

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE')
)

class GenderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['gender']

class SignUpForm(UserCreationForm):        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

class CustomerUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    class Meta:
        model = User
        fields = ['username', 'first_name']        
        