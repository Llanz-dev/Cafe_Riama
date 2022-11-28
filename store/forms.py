from .models import OrderItem, Delivery, Collection, Payment
from django import forms

CHOICES=(('Hot', 'Hot'),
         ('Cold', 'Cold'))

class CaffeinatedForm(forms.ModelForm):
    hot_or_cold = forms.ChoiceField(label='', choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CaffeinatedForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = OrderItem
        fields = ['hot_or_cold', 'milk', 'whip_cream', 'syrup_pump', 'espresso_shot']
        
class CoolersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CoolersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = []
        
class OnlyWaterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OnlyWaterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = ['bottled_water']

class DeliveryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = Delivery
        fields = '__all__'
        widgets = {
          'other_notes': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        labels = {
            'fullname': 'Full name',
            'location': 'House Number, Building and Street Name'
        }
        
class CollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = Collection
        fields = '__all__'
        widgets = {
          'other_notes': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        labels = {
            'fullname': 'Full name',
        }

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
            self.fields['subtotal'].label = ""
            self.fields['delivery_fee'].label = ""
            self.fields['total'].label = ""     
                   
    class Meta:
        model = Payment
        fields = '__all__'   
        labels = {
            'subtotal': '',
            'delivery_fee': '',
            'total': ''
        }