from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models

CATEGORY_CHOICES = (
    ('Coffee Classics', 'Coffee Classics'),
    ('Special Latte', 'Special Latte'),
    ('Frappe', 'Frappe'),
    ('Other Drinks', 'Other Drinks'),
    ('Starters', 'Starters'),
    ('Silog Meals', 'Silog Meals'),
    ('Burger with Fries', 'Burger with Fries'),
    ('All About Wings', 'All About Wings'),
    ('Pasta', 'Pasta'),
    ('Pizza', 'Pizza'),
    ('Main Course', 'Main Course'),
    ('Sizzlers', 'Sizzlers')
)

CHOICES=[('Hot', 'Hot'),
         ('Cold', 'Cold')]

class CaffeinatedAdd(models.Model):
    milk = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    whip_cream = models.PositiveSmallIntegerField(default=30, blank=True, null=True)
    syrup_pump = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    espresso_shot = models.PositiveSmallIntegerField(default=40, blank=True, null=True)

# Create your models here.
class Item(models.Model):
    customer = models.ManyToManyField(User, blank=True, null=True)
    name = models.CharField(max_length=50)
    hot_price = models.PositiveIntegerField(default=0)
    cold_price = models.PositiveIntegerField(default=0)
    hot_cold = models.CharField(choices=CHOICES, max_length=5, default='Hot')
    caffeinated_add = models.ForeignKey(CaffeinatedAdd, blank=True, null=True, on_delete=models.SET_NULL)
    milk = models.BooleanField(default=False)
    whip_cream = models.BooleanField(default=False)
    syrup_pump = models.BooleanField(default=False)
    espresso_shot = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=17, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='Lorem ipsum dolor sit amet consectetur adipisicing elit. Quia animi eveniet recusandae. Assumenda ab aliquid deleniti voluptatibus officia. Debitis, quam.')
    item_slug = models.SlugField(unique=True, default=None)
    image = models.ImageField(default='constant/cafe.jpg', upload_to='items-img')

    def __str__(self):
        return self.name

    def product_detail_url(self):
        return reverse('store:product-detail', kwargs={'item_slug': self.item_slug})
    
    def increase_quantity(self):
        return reverse('store:increase-quantity', kwargs={'item_slug': self.item_slug})    
    
    def decrease_quantity(self):
        return reverse('store:decrease-quantity', kwargs={'item_slug': self.item_slug})    

    def save(self, *args, **kwargs):
        self.item_slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    hot_or_cold = models.CharField(choices=CHOICES, max_length=5, default='Hot')    
    milk = models.BooleanField(default=False)
    whip_cream = models.BooleanField(default=False)
    syrup_pump = models.BooleanField(default=False)
    espresso_shot = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    hot_cold = models.CharField(max_length=4, default='')
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    ordered = models.BooleanField(default=False)
    in_cart = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.item.name} - {self.quantity}'

    def get_total_item_price(self):   
        return self.quantity * self.total_price 
      
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.items.count()}'

DISTRICT_CHOICES = (
    ('City Proper', 'City Proper'),
    ('Arevalo', 'Arevalo'),
    ('La Paz', 'La Paz'),
    ('Lapuz', 'Lapuz'),
    ('Mandurriao', 'Mandurriao'),
    ('Molo', 'Molo')
)

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=80)
    location = models.CharField(max_length=90)
    mobile_number = models.CharField(max_length=11)
    districts = models.CharField(choices=DISTRICT_CHOICES, max_length=11, default='City Proper')
    label = models.CharField(max_length=20, blank=True, null=True)
    other_notes = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self): 
        return f'{self.user.username} - {self.districts}'
    
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=80)
    mobile_number = models.CharField(max_length=11)
    other_notes = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.fullname}'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, blank=True, null=True)
    collection = models.OneToOneField(Collection, on_delete=models.CASCADE, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    subtotal = models.PositiveIntegerField(blank=True, null=True)
    delivery_fee = models.PositiveIntegerField(default=0, blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)
    ordered_date = models.DateTimeField(default=timezone.now)    
    finish_transaction = models.BooleanField(default=False, blank=True, null=True)
    
    def __str__(self):
        return f'{self.total}'