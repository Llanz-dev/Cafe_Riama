from django.contrib import admin
from .models import AddOn, Item, FavoriteItem, OrderItem, Order, Delivery, Collection, DeliveryFee, Payment

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'item_slug': ['name'],
    }

# Register your models here.
admin.site.register(AddOn)
admin.site.register(Item, ItemAdmin)
admin.site.register(FavoriteItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Collection)
admin.site.register(DeliveryFee)
admin.site.register(Payment)
