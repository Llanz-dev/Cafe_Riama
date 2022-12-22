from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('all-product/', views.all_product, name='all-product'),
    path('favorite-list/', views.favorite_list, name='favorite-list'),
    path('add-favorite/<slug:item_slug>/', views.add_favorite, name='add-favorite'),
    path('remove-favorite/<slug:item_slug>/', views.remove_favorite, name='remove-favorite'),
    path('product-detail/Caffeinated/<slug:item_slug>/', views.detail_caffeinated, name='caffeinated'),
    path('product-detail/Coolers/<slug:item_slug>/', views.detail_coolers, name='coolers'),
    path('product-detail/main/<slug:item_slug>/', views.detail_main, name='main'),    
    path('product-detail/pizza/<slug:item_slug>/', views.detail_pizza, name='pizza'),    
    path('product-detail/<str:category>/<slug:item_slug>/', views.detail_only_water, name='detail-only-water'),
    path('product-update/caffeinated/<slug:item_slug>/<int:order_item_id>/', views.caffeinated_update, name='caffeinated-update'),
    path('product-update/pizza/<slug:item_slug>/<int:order_item_id>/', views.pizza_update, name='pizza-update'),
    path('product-update/main/<slug:item_slug>/<int:order_item_id>/', views.main_update, name='main-update'),
    path('product-update/<str:category>/<slug:item_slug>/<int:order_item_id>/', views.only_water_update, name='only-water-update'),
    path('specific-category/<str:item_category>/', views.specific_category, name='specific-category'),
    path('cart/', views.cart, name='cart'),
    path('increase-quantity/<slug:item_slug>/<int:order_item_id>/', views.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<slug:item_slug>/<int:order_item_id>/', views.decrease_quantity, name='decrease-quantity'),
    path('remove-product/<slug:item_slug>/<int:order_item_id>/', views.remove_product, name='remove-product'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/delivery/', views.delivery, name='delivery'),
    path('checkout/collection/', views.collection, name='collection'),
    path('checkout/thank-you/', views.thank_you, name='thank-you'),
    path('pending-orders/', views.pending_orders, name='pending-orders')
]