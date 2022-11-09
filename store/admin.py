from django.contrib import admin
from .models import Item, OrderItem, Order, Delivery, Collection, Payment

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'item_slug': ['name'],
    }

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Collection)
admin.site.register(Payment)
