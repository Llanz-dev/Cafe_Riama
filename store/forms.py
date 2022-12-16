from .models import OrderItem, Delivery, Collection, Payment
from django import forms

CHOICES=(('Hot', 'Hot'),
         ('Cold', 'Cold'))

# This form is only for the category of Caffeinated.
class CaffeinatedForm(forms.ModelForm):
    hot_or_cold = forms.ChoiceField(label='', choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CaffeinatedForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = OrderItem
        fields = ['hot_or_cold', 'milk', 'whip_cream', 'syrup_pump', 'espresso_shot']

# This form is only for the category of Coolers.
class CoolersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CoolersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = []

# This form is only for the the following categories: Starters, Silog Meals, Burger with Fries and Pasta.
class OnlyWaterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OnlyWaterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = ['bottled_water']

# This form is only for the category of Pizza.
class PizzaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PizzaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = ['bacon', 'pepperoni', 'ham', 'cheese']   
        
# This form is for the following of categories: All About Wings, Main Course and Sizzlers.
class MainForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'
    class Meta:
        model = OrderItem
        fields = ['plain_rice', 'rice_platter', 'aligue_platter', 'bottled_water']   

class DeliveryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-light'

    class Meta:
        model = Delivery
        fields = '__all__'
        exclude = ['maximum_delivery_fee']
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