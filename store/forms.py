from .models import Item, Delivery, Collection, Payment
from django import forms

CHOICES=(('Hot', 'Hot'),
         ('Cold', 'Cold'))

class CaffeinatedForm(forms.ModelForm):
    hot_cold = forms.ChoiceField(label='', choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CaffeinatedForm, self).__init__(*args, **kwargs)
        self.fields['hot_cold'].widget.attrs['class'] = 'form-check-input'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = Item
        exclude = ['name', 'hot_price', 'cold_price', 'caffeinated_add', 'discount_price', 'category', 'description', 'item_slug', 'image']
        fields = '__all__'
                        
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