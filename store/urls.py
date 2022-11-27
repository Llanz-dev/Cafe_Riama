from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('all-product/', views.all_product, name='all-product'),
    path('product-detail/caffeinated/<slug:item_slug>/', views.detail_caffeinated, name='caffeinated'),
    path('product-detail/coolers/<slug:item_slug>/', views.detail_coolers, name='coolers'),
    path('product-update/<slug:item_slug>/<int:order_item_id>/', views.product_update, name='product-update'),
    path('specific-category/<str:item_category>/', views.specific_category, name='specific-category'),
    path('cart/', views.cart, name='cart'),
    path('buy-now/<slug:item_slug>/', views.buy_now, name='buy-now'),
    path('increase-quantity/<slug:item_slug>/<int:order_item_id>/', views.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<slug:item_slug>/<int:order_item_id>/', views.decrease_quantity, name='decrease-quantity'),
    path('remove-product/<slug:item_slug>/<int:order_item_id>/', views.remove_product, name='remove-product'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/delivery/', views.delivery, name='delivery'),
    path('checkout/collection/', views.collection, name='collection'),
    path('checkout/thank-you/', views.thank_you, name='thank-you'),
    path('pending-orders/', views.pending_orders, name='pending-orders')
]