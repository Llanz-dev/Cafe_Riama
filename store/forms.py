from django import forms
from django import forms
from .models import Item, Delivery, Collection, Payment

class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = Item
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