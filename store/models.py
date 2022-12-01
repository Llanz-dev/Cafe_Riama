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

class AddOn(models.Model):
    plain_rice = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    rice_platter = models.PositiveSmallIntegerField(default=100, blank=True, null=True)
    aligue_platter = models.PositiveSmallIntegerField(default=120, blank=True, null=True)
    milk = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    whip_cream = models.PositiveSmallIntegerField(default=30, blank=True, null=True)
    syrup_pump = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    espresso_shot = models.PositiveSmallIntegerField(default=40, blank=True, null=True)    
    bacon = models.PositiveSmallIntegerField(default=30, blank=True, null=True)
    pepperoni = models.PositiveSmallIntegerField(default=40, blank=True, null=True)
    ham = models.PositiveSmallIntegerField(default=30, blank=True, null=True)
    cheese = models.PositiveSmallIntegerField(default=50, blank=True, null=True)
    plain_rice = models.PositiveSmallIntegerField(default=30, blank=True, null=True)
    rice_platter = models.PositiveSmallIntegerField(default=100, blank=True, null=True)
    aligue_platter = models.PositiveSmallIntegerField(default=120, blank=True, null=True)
    bottled_water = models.PositiveSmallIntegerField(default=20, blank=True, null=True)
    
# Create your models here.
class Item(models.Model):
    customer = models.ManyToManyField(User, blank=True, null=True)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)    
    hot_price = models.PositiveIntegerField(default=0)
    cold_price = models.PositiveIntegerField(default=0)
    hot_cold = models.CharField(choices=CHOICES, max_length=5, default='Hot')
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=17, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='Lorem ipsum dolor sit amet consectetur adipisicing elit. Quia animi eveniet recusandae. Assumenda ab aliquid deleniti voluptatibus officia. Debitis, quam.')
    item_slug = models.SlugField(unique=True, default=None)
    image = models.ImageField(default='constant/cafe.jpg', upload_to='items-img')

    def __str__(self):
        return self.name
    
    # URL of this function is for the category of Caffeinated.
    def detail_caffeinated_url(self):
        return reverse('store:caffeinated', kwargs={'item_slug': self.item_slug})

    # URL of this function is for the category of Coolers.
    def detail_coolers_url(self):
        return reverse('store:coolers', kwargs={'item_slug': self.item_slug})
    
    # URL of this function is for the category of Coolers.
    def detail_coolers_url(self):
        return reverse('store:coolers', kwargs={'item_slug': self.item_slug})

    # URL of the items that are only bottled water is their options.
    # The categories that are belong to this is the following: Starters, Silog Meals, Burger with Fries, and Pasta.
    def detail_only_water_url(self):
        return reverse('store:detail-only-water', kwargs={'category': self.category, 'item_slug': self.item_slug})

    # URL of this function is for the category of Pizza.    
    def detail_pizza_url(self):
        return reverse('store:pizza', kwargs={'item_slug': self.item_slug})
    
    # URL of this function is for the categories of the following: All About Wings, Main Course and Sizzlers.    
    def detail_main_url(self):
        return reverse('store:main', kwargs={'item_slug': self.item_slug})
    
    # URL of this function is for the increase quantity of the items.
    def increase_quantity(self):
        return reverse('store:increase-quantity', kwargs={'item_slug': self.item_slug})    

    # URL of this function is for the decrease quantity of the items.    
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
    bacon = models.BooleanField(default=False)
    pepperoni = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    cheese = models.BooleanField(default=False)
    plain_rice = models.BooleanField(default=False)
    rice_platter = models.BooleanField(default=False)
    aligue_platter = models.BooleanField(default=False)
    bottled_water = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs):
        """ This step is just formatting: add the dash if missing """
        if '-' not in self.mobile_number:
            self.mobile_number = '{0}-{1}-{2}'.format(
                 self.mobile_number[:4], self.mobile_number[4:7], self.mobile_number[7:])
        # Continue the model saving
        super(Delivery, self).save(*args, **kwargs)  
    
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=80)
    mobile_number = models.CharField(max_length=11)
    other_notes = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.fullname}'

    def save(self, *args, **kwargs):
        if '-' not in self.mobile_number:
            self.mobile_number = '{0}-{1}-{2}'.format(
                 self.mobile_number[:4], self.mobile_number[4:7], self.mobile_number[7:])
            # Continue the model saving
            super(Collection, self).save(*args, **kwargs) 

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