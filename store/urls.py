from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('all-product/', views.all_product, name='all-product'),
    path('product-detail/<slug:item_slug>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('buy-now/<slug:item_slug>/', views.buy_now, name='buy-now'),
    path('add-to-cart/<slug:item_slug>/', views.add_to_cart, name='add-to-cart'),
    path('increase-quantity/<slug:item_slug>/', views.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<slug:item_slug>/', views.decrease_quantity, name='decrease-quantity'),
    path('remove-product/<slug:item_slug>/', views.remove_product, name='remove-product'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/delivery/', views.delivery, name='delivery'),
    path('checkout/collection/', views.collection, name='collection'),
    path('checkout/thank-you/', views.thank_you, name='thank-you'),
    path('pending-orders/', views.pending_orders, name='pending-orders')
]