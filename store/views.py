from .models import Item, OrderItem, Order, Delivery, Collection, Payment
from .forms import CaffeinatedForm, PaymentForm, DeliveryForm, CollectionForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def order_quantity(request):
    if request.user.is_authenticated:
        customer = Order.objects.filter(user=request.user, ordered=False)
        if customer.exists():                    
            return customer.first().items.all().count()
    else:
        return 0

def sub_total(request):
    order = Order.objects.filter(user=request.user, ordered=False)    
    customer_order = order.first()   
    if customer_order:
        all_order = customer_order.items.all().order_by('-id')  
        total = 0
        for item in all_order:
            # If it is the quantity of item is zero then it will delete to the OrderItem table.
            if item.quantity <= 0:
                order_item = OrderItem.objects.get(item=item.item)
                customer_order.items.remove(order_item)
            # Calculate the total of order product.                
            total += item.get_total_item_price()  
        return total
    else:
        return 0

def home(request):    
    items_caffeinated_two = Item.objects.filter(category='Coffee Classics')[:2]
    items_caffeinated_four = Item.objects.filter(category='Coffee Classics')[2:4]
    items_frappe_two = Item.objects.filter(category='Frappe')[:2]
    items_frappe_four = Item.objects.filter(category='Frappe')[2:4]
    items_starters_two = Item.objects.filter(category='Starters')[:2]
    items_starters_four = Item.objects.filter(category='Starters')[2:4]
    items_silog_two = Item.objects.filter(category='Silog Meals')[:2]
    items_silog_four = Item.objects.filter(category='Silog Meals')[2:4]
    items_burger_two = Item.objects.filter(category='Burger with Fries')[:2]
    items_wings_two = Item.objects.filter(category='All About Wings')[:2]
    items_wings_four = Item.objects.filter(category='All About Wings')[2:4]
    items_pasta_two = Item.objects.filter(category='Pasta')[:2]
    items_pasta_four = Item.objects.filter(category='Pasta')[2:4]
    items_pizza_two = Item.objects.filter(category='Pizza')[:2]
    items_pizza_four = Item.objects.filter(category='Pizza')[2:4]
    items_main_two = Item.objects.filter(category='Main Course')[:2]
    items_main_four = Item.objects.filter(category='Main Course')[2:4]
    items_sizzlers_two = Item.objects.filter(category='Sizzlers')[:2]    
    items_sizzlers_four = Item.objects.filter(category='Sizzlers')[2:4]  

    already_in_cart = None
    customer_order_item = None
    if request.user.is_authenticated:
        for item in items_caffeinated_two:
            order_item = OrderItem.objects.filter(user=request.user, in_cart=True, ordered=False)        
            if order_item.exists():  
                already_in_cart = order_item                                                          
                
    for item in items_caffeinated_two:            
        print(item.name, ':', item.customer.filter(username=request.user).exists())
        
    context = {
        'already_in_cart': already_in_cart,
        'items_caffeinated_two': items_caffeinated_two, 
        'items_caffeinated_four': items_caffeinated_four, 
        'items_frappe_two': items_frappe_two, 
        'items_frappe_four': items_frappe_four, 
        'items_starters_two': items_starters_two, 
        'items_starters_four': items_starters_four, 
        'items_silog_two': items_silog_two, 
        'items_silog_four': items_silog_four, 
        'items_burger_two': items_burger_two, 
        'items_wings_two': items_wings_two, 
        'items_wings_four': items_wings_four, 
        'items_pasta_two': items_pasta_two, 
        'items_pasta_four': items_pasta_four, 
        'items_pizza_two': items_pizza_two, 
        'items_pizza_four': items_pizza_four, 
        'items_main_two': items_main_two, 
        'items_main_four': items_main_four, 
        'items_sizzlers_two': items_sizzlers_two,
        'items_sizzlers_four': items_sizzlers_four,
        'order_quantity': order_quantity(request)
        }    

    return render(request, 'store/home.html', context)

def product_detail(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)                                        
    caffeinated_form = CaffeinatedForm()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            caffeinated_form = CaffeinatedForm(request.POST)
            if caffeinated_form.is_valid():
                instance = caffeinated_form.save(commit=False)
                instance.user = request.user
                instance.item = item
                instance.hot_or_cold = caffeinated_form.cleaned_data['hot_or_cold']           

                if caffeinated_form.cleaned_data['hot_or_cold'] == 'Hot':
                    instance.price = item.hot_price
                else:
                    instance.price = item.cold_price

                instance.hot_cold = caffeinated_form.cleaned_data['hot_or_cold']           

                if caffeinated_form.cleaned_data['milk']:
                    instance.milk = True
                elif caffeinated_form.cleaned_data['whip_cream']:
                    instance.whip_cream = True
                elif caffeinated_form.cleaned_data['syrup_pump']:
                    instance.syrup_pump = True
                elif caffeinated_form.cleaned_data['espresso_shot']:
                    instance.espresso_shot = True     

                add_on_list = [instance.milk, instance.whip_cream, instance.syrup_pump, instance.espresso_shot]

                for data in range(4):
                    if data == 0 and add_on_list[0]:
                        instance.total_price += item.caffeinated_add.milk
                    elif data == 1 and add_on_list[1]:
                        instance.total_price += item.caffeinated_add.whip_cream
                    elif data == 2 and add_on_list[2]:
                        instance.total_price += item.caffeinated_add.syrup_pump
                    elif data == 3 and add_on_list[3]:
                        instance.total_price += item.caffeinated_add.espresso_shot

                instance.total_price += instance.price
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)                 
                order.items.add(caffeinated_form.save())   
                instance.in_cart = True   
                item.customer.add(request.user)
                item.save()                                              
                instance.save()                                       
                print('Success')
            else:
                print('Error')

            return redirect('store:cart')     
        else:
            return redirect('account:sign-in')                      

        # order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, price=price, hot_cold=caffeinated, ordered=False)
        # order_qs = Order.objects.filter(user=request.user, ordered=False)

        # if order_qs.exists():
        #     order = order_qs[0]   
        #     if order.items.filter(item__item_slug=item.item_slug).exists():
        #         print('Order items:', order.items.filter(item__item_slug=item.item_slug))
        #         order_item.quantity += 1
        #         order_item.save()    
        #     else:
        #         order.items.add(order_item)        
        # else:
        #     order = Order.objects.create(user=request.user, ordered=False)                 
        #     order.items.add(order_item)     

        # return redirect('store:cart')
        
    context = {'item': item, 'caffeinated_form': caffeinated_form, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context)

def product_update(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)
    order_item = OrderItem.objects.get(user=request.user, item=item, ordered=False)
    caffeinated_form = CaffeinatedForm(instance=order_item)
    if request.method == 'POST':
        caffeinated_form = CaffeinatedForm(request.POST, instance=order_item)
        order_qs = Order.objects.filter(user=request.user, ordered=False)            
        if caffeinated_form.is_valid():
            instance = caffeinated_form.save(commit=False)
            instance.hot_or_cold = caffeinated_form.cleaned_data['hot_or_cold']           
            
            if caffeinated_form.cleaned_data['hot_or_cold'] == 'Hot':
                instance.price = item.hot_price
            else:
                instance.price = item.cold_price

            instance.hot_cold = caffeinated_form.cleaned_data['hot_or_cold']           
            
            if caffeinated_form.cleaned_data['milk']:
                instance.milk = True
            elif caffeinated_form.cleaned_data['whip_cream']:
                instance.whip_cream = True
            elif caffeinated_form.cleaned_data['syrup_pump']:
                instance.syrup_pump = True
            elif caffeinated_form.cleaned_data['espresso_shot']:
                instance.espresso_shot = True     

            add_on_list = [instance.milk, instance.whip_cream, instance.syrup_pump, instance.espresso_shot]
            instance.total_price = 0
            for data in range(4):
                if data == 0 and add_on_list[0]:
                    instance.total_price += item.caffeinated_add.milk
                elif data == 1 and add_on_list[1]:
                    instance.total_price += item.caffeinated_add.whip_cream
                elif data == 2 and add_on_list[2]:
                    instance.total_price += item.caffeinated_add.syrup_pump
                elif data == 3 and add_on_list[3]:
                    instance.total_price += item.caffeinated_add.espresso_shot
                    
            instance.total_price += instance.price                    
            instance.save()                                                    
        else:
            print('Error')
            
        return redirect('store:cart')
    
    context = {'item':item, 'caffeinated_form': caffeinated_form, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-update.html', context)

def all_product(request):
    coffee_classics = Item.objects.filter(category='Coffee Classics')
    special_latte = Item.objects.filter(category='Special Latte')
    frappe = Item.objects.filter(category='Frappe')
    other_drinks = Item.objects.filter(category='Other Drinks')
    starters = Item.objects.filter(category='Starters')
    silog_meals = Item.objects.filter(category='Silog Meals')
    burger_fries = Item.objects.filter(category='Burger with Fries')
    wings = Item.objects.filter(category='All About Wings')
    pasta = Item.objects.filter(category='Pasta')
    pizza = Item.objects.filter(category='Pizza')
    main_course = Item.objects.filter(category='Main Course')
    sizzlers = Item.objects.filter(category='Sizzlers')    

    context = {'coffee_classics': coffee_classics, 
               'special_latte': special_latte,
               'other_drinks': other_drinks,
               'frappe': frappe, 
               'starters': starters, 
               'silog_meals': silog_meals,
               'burger_fries': burger_fries,
               'wings': wings,
               'pasta': pasta,
               'pizza': pizza,
               'main_course': main_course,
               'sizzlers': sizzlers,
               'order_quantity': order_quantity(request)
               }
    
    return render(request, 'store/all-product.html', context)

def specific_category(request, item_category):
    categorized_items = None
    items_category = None
    coffee_classics = None
    special_latte = None
    frappe = None
    other_drinks = None
    
    if item_category == 'Caffeinated':
        coffee_classics = Item.objects.filter(category='Coffee Classics')
        special_latte = Item.objects.filter(category='Special Latte')
        items_category = item_category
    elif item_category == 'Coolers':
        frappe = Item.objects.filter(category='Frappe')
        other_drinks = Item.objects.filter(category='Other Drinks')
        items_category = item_category
    else:
        categorized_items = Item.objects.filter(category=item_category)
        items_category = categorized_items.first().category

    context = {'categorized_items': categorized_items, 'items_category': items_category, 'coffee_classics': coffee_classics, 'special_latte': special_latte, 'other_drinks': other_drinks, 'frappe': frappe}
    return render(request, 'store/specific-category.html', context)    

@login_required
def buy_now(request, item_slug):
    print('You clicked buy now!')
        
    return redirect('store:product-detail', item_slug=item_slug)

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, ordered=False)    
    
    if order.exists():
        customer_order = order.first()
        all_order = customer_order.items.all().order_by('-id')              
        # Delete the customer in Order table if he or she has no order left in cart.
        order_count = customer_order.items.all().count()                      
        if order_count == 0:
            Order.objects.get(user=request.user, ordered=False).delete()
            
        context = {'customer_exists': order.exists(), 'all_order': all_order, 'order_quantity': order_quantity(request), 'sub_total': sub_total(request), 'count_order': order_count}
    else:        
        context = {'customer_exists': order.exists()}
        
    return render(request, 'store/cart.html', context)

def update_item(request, item_slug):
    pass

@login_required
def decrease_quantity(request, item_slug): 
    item = get_object_or_404(Item, item_slug=item_slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]    
        # Check if the order item is in the order.       
        if order.items.filter(item__item_slug=item.item_slug).exists():
            order_item.quantity -= 1
            order_item.save()
            # If the order item quantity is zero then delete in order item table.
            if order_item.quantity == 0:
                order_item.delete()     
                item.customer.remove(request.user)                   
                
    return redirect('store:cart')         

@login_required
def increase_quantity(request, item_slug): 
    item = get_object_or_404(Item, item_slug=item_slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]    
        # Check if the order item is in the order
        if order.items.filter(item__item_slug=item.item_slug).exists():
            order_item.quantity += 1
            order_item.save()    
        else:
            order.items.add(order_item)        
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
             
    return redirect('store:cart')   
     
@login_required
def remove_product(request, item_slug):
    item = get_object_or_404(Item, item_slug=item_slug)    
    item.customer.remove(request.user)                       
    OrderItem.objects.get(user=request.user, item=item, ordered=False).delete()
    
    return redirect('store:cart')       

@login_required
def delivery(request):
    payment = Payment.objects.all()
    delivery_fee = payment.first().delivery_fee
    delivery_form = DeliveryForm()
    order = Order.objects.filter(user=request.user, ordered=False) 
    order_items = OrderItem.objects.filter(user=request.user, ordered=False) 

    # If the customer has no order yet.
    if not order.exists():
        context = {'customer_exists': order.exists()}   
        return render(request, 'store/delivery.html', context)     

    # Get the customer orders. Calculate subtotal and total.
    customer_order = order.first() 
    customer_items = order_items.all() 
    print('Customer order:', customer_items)
    
    all_order = customer_order.items.all().order_by('-id') 
    total = delivery_fee + sub_total(request)
    subtotal = sub_total(request)

    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)       
        office_home = request.POST.get('home-office') 
        print('Office home:', office_home)                         
        if delivery_form.is_valid():
            instance = delivery_form.save(commit=False)
            instance.user = request.user            
            instance.label = office_home
            instance.order = customer_order
            if instance.label:  
                customer_order.ordered = True
                # This will make the ordered field equals to True in OrderItem table.
                for product in customer_items:
                    product.ordered = True
                    product.save()
                customer_order.save()
                instance.save()
                Payment.objects.create(user=request.user, delivery=delivery_form.instance, order=customer_order, subtotal=subtotal, delivery_fee=delivery_fee, total=total)  
                return redirect('store:thank-you') 
            else:
                messages.error(request, 'Please select a label between label or home')      

    context = {'customer_exists': order.exists(), 'delivery_form': delivery_form, 'delivery_fee': delivery_fee, 'all_order': all_order, 'sub_total': sub_total(request), 'total': total, 'order_quantity': order_quantity(request)}
    return render(request, 'store/delivery.html', context)

@login_required
def collection(request):
    collection_form = CollectionForm()
    order = Order.objects.filter(user=request.user, ordered=False)     
    order_items = OrderItem.objects.filter(user=request.user, ordered=False) 

    # Get the customer orders. Calculate subtotal and total.    
    # The subtotal and total is the same due to had no delivery fee charge.
    customer_order = order.first()    
    customer_items = order_items.all() 
    for data in customer_items:
        print('Data:', data)     
    all_order = customer_order.items.all().order_by('-id')    
    total = sub_total(request)
    
    # If the customer has no order yet.
    if not order.exists():
        context = {'customer_exists': order.exists()}   
        return render(request, 'store/delivery.html', context)    

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)               
        if collection_form.is_valid():
            instance = collection_form.save(commit=False)
            instance.user = request.user
            # This will make the ordered field equals to True in OrderItem table.
            for product in customer_items:
                product.ordered = True
                product.save()
            customer_order.ordered = True
            customer_order.save()
            instance.save()
            Payment.objects.create(user=request.user, collection=collection_form.instance, order=customer_order, subtotal=total, total=total)              
            return redirect('store:thank-you')             

    context = {'customer_exists': order.exists(), 'collection_form': collection_form, 'all_order': all_order, 'total': sub_total(request), 'order_quantity': order_quantity(request)}
    return render(request, 'store/collection.html', context)

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, ordered=False) 
       
    # If the customer has no order yet.
    if not order.exists():
        context = {'customer_exists': order.exists()}   
        return render(request, 'store/delivery.html', context)   

    # All the customer order will display on right side navigation.
    all_order = order.first().items.all().order_by('-id') 
    
    context = {'customer_exists': order.exists(), 'order_quantity': order_quantity(request), 'all_order': all_order}
    return render(request, 'store/checkout.html', context)

# After you place your order.
@login_required
def thank_you(request):
    return render(request, 'store/thank-you.html')    

# This where your pending orders show.
@login_required
def pending_orders(request):
    # This will get all what you ordered and display the information that you input.
    all_order = Order.objects.filter(user=request.user, ordered=True)    
    
    # The pending orders will appear as long as you don't claim or we didn't delivered yet.
    # The admin has only the access to make the finish_transaction field turns to True.
    payment = Payment.objects.filter(user=request.user, finish_transaction=False).order_by('-id') 

    # If the customer has no order yet.
    if not all_order.exists():
        context = {'customer_exists': all_order.exists()}   
        return render(request, 'store/delivery.html', context)              
    
    context = {'customer_exists': all_order.exists(), 'all_order': all_order, 'payment': payment, 'order_quantity': order_quantity(request)}
    return render(request, 'store/pending-orders.html', context)
