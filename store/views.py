from .models import Item, OrderItem, Order, Delivery, Collection, Payment
from account.models import Customer
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

    context = {
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
    order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)
    
    # Fix this
    # print(order_item.exists())
    # for data in order_item:
    #     print(data.item.name, data.hot_or_cold)
    # -----------
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            caffeinated_form = CaffeinatedForm(request.POST)
            if caffeinated_form.is_valid():
                instance = caffeinated_form.save(commit=False)
                instance.user = request.user
                instance.item = item
                instance.hot_or_cold = caffeinated_form.cleaned_data['hot_or_cold']           

                # This will set the price whether the customer wants Hot or Cold.
                if caffeinated_form.cleaned_data['hot_or_cold'] == 'Hot':
                    instance.price = item.hot_price
                else:
                    instance.price = item.cold_price

                instance.hot_cold = caffeinated_form.cleaned_data['hot_or_cold']           

                # This will check the checkbox if the customer would like to add an add-ons.
                # Also to add the price and total it.
                if caffeinated_form.cleaned_data['milk']:
                    instance.total_price += item.caffeinated_add.milk
                    instance.milk = True
                if caffeinated_form.cleaned_data['whip_cream']:
                    instance.total_price += item.caffeinated_add.whip_cream
                    instance.whip_cream = True
                if caffeinated_form.cleaned_data['syrup_pump']:
                    instance.total_price += item.caffeinated_add.syrup_pump
                    instance.syrup_pump = True
                if caffeinated_form.cleaned_data['espresso_shot']:
                    instance.espresso_shot = True     
                    instance.total_price += item.caffeinated_add.espresso_shot
                
                if order_item:                    
                    # If the the product has only 1 in OrderItem table.
                    if order_item.count() == 1:
                        order_item = order_item.last()
                        # If the customer go back again on the specific product and he or she click again the "Add to Cart" button.
                        # Then it will check first if he or she still wants to buy the same add-ons.
                        # If he or she is, then it will just increment the quantity of this product.
                        if instance.hot_or_cold == order_item.hot_or_cold and order_item.milk == instance.milk and order_item.whip_cream == instance.whip_cream and order_item.syrup_pump == instance.syrup_pump and order_item.espresso_shot == instance.espresso_shot:
                            order_item.quantity += 1
                            order_item.save()
                            return redirect('store:cart')  
                    # If the the product has only 1 in OrderItem table.             
                    else:
                        for data in order_item:
                            if instance.hot_or_cold == data.hot_or_cold and data.milk == instance.milk and data.whip_cream == instance.whip_cream and data.syrup_pump == instance.syrup_pump and data.espresso_shot == instance.espresso_shot:
                                data.quantity += 1
                                data.save()
                                return redirect('store:cart')      
                                                                                
                # This will add to OrderItem table and input whatever the customer added.
                instance.total_price += instance.price
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)                 
                order.items.add(caffeinated_form.save())   
                instance.in_cart = True   
                item.customer.add(request.user)
                item.save()                                              
                instance.save()                                       

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

def product_update(request, item_slug, order_item_id):
    item = Item.objects.get(item_slug=item_slug)
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)
    
    caffeinated_form = CaffeinatedForm(instance=order_item)
    if request.method == 'POST':
        caffeinated_form = CaffeinatedForm(request.POST, instance=order_item)
        if caffeinated_form.is_valid():
            instance = caffeinated_form.save(commit=False)
            instance.hot_or_cold = caffeinated_form.cleaned_data['hot_or_cold']           
            
            if caffeinated_form.cleaned_data['hot_or_cold'] == 'Hot':
                instance.price = item.hot_price
            else:
                instance.price = item.cold_price

            instance.hot_cold = caffeinated_form.cleaned_data['hot_or_cold']           

            # This update among add-ons.
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
    
    context = {'item':item, 'order_item': order_item, 'caffeinated_form': caffeinated_form, 'order_quantity': order_quantity(request)}
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

    context = {'categorized_items': categorized_items, 'items_category': items_category, 'coffee_classics': coffee_classics, 'special_latte': special_latte, 'other_drinks': other_drinks, 'frappe': frappe, 'order_quantity': order_quantity(request)}
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

@login_required
def decrease_quantity(request, item_slug, order_item_id): 
    item = get_object_or_404(Item, item_slug=item_slug)
    order_item = OrderItem.objects.get(user=request.user, id=order_item_id, item=item, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item_count = OrderItem.objects.filter(user=request.user, item=item, ordered=False).count()
    
    if order_qs.exists():
        order = order_qs[0]    
        # Check if the order item is in the order.       
        if order.items.filter(item__item_slug=item.item_slug).exists():
            order_item.quantity -= 1
            order_item.save()
            # When the order item quantity is zero then delete in order item table.
            # If the customer has only 1 the same product left then delete the Item object in OrderItem Table and remove also the customer to that product. 
            if order_item.quantity == 0 and order_item_count == 1:
                order_item.delete()     
                item.customer.remove(request.user)                   
            # If not, then remove only the Item in OrderItem table.
            if order_item.quantity == 0 and order_item_count > 1:
                order_item.delete()                     
                
    return redirect('store:cart')         

@login_required
def increase_quantity(request, item_slug, order_item_id): 
    item = get_object_or_404(Item, item_slug=item_slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, id=order_item_id, item=item, ordered=False)
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
def remove_product(request, item_slug, order_item_id):
    item = get_object_or_404(Item, item_slug=item_slug)        
    order_item = OrderItem.objects.get(user=request.user, id=order_item_id, item=item, ordered=False)    
    order_item_count = OrderItem.objects.filter(user=request.user, item=item, ordered=False).count()    
    print('order_item quantity:', order_item.quantity)
    print('order_item_count:', order_item_count)
    # When the order item quantity is zero then delete in order item table.
    # If the customer has only 1 the same product left then delete the Item object in OrderItem Table and remove also the customer to that product. 
    if order_item_count == 1:
        item.customer.remove(request.user)                       
        OrderItem.objects.get(user=request.user, id=order_item_id, item=item, ordered=False).delete()
    # If not, then remove only the Item in OrderItem table.        
    if order_item_count > 1:
        order_item.delete()
        
    return redirect('store:cart')       

@login_required
def delivery(request):
    payment = Payment.objects.all()
    delivery_fee = payment.first().delivery_fee
    delivery_form = DeliveryForm()
    order = Order.objects.filter(user=request.user, ordered=False) 
    order_items = OrderItem.objects.filter(user=request.user, ordered=False, in_cart=True) 

    # If the customer has no order yet.
    if not order.exists():
        context = {'customer_exists': order.exists()}   
        return render(request, 'store/delivery.html', context)     

    # Get the customer orders. Calculate subtotal and total.
    customer_order = order.first() 
    customer_items = order_items.all() 
    
    all_order = customer_order.items.all().order_by('-id') 
    total = delivery_fee + sub_total(request)
    subtotal = sub_total(request)

    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)       
        office_home = request.POST.get('home-office') 
        if delivery_form.is_valid():
            instance = delivery_form.save(commit=False)
            # This set of the customer.
            instance.user = request.user            
            instance.label = office_home
            # This set of the customer Order table.
            instance.order = customer_order
            if instance.label:  
                customer_order.ordered = True
                # This will make the "ordered" and "in_cart" field equals to True in OrderItem table.            
                for product in customer_items:
                    product.ordered = True
                    product.in_cart = False
                    product.save()
                # Remove all the product that customer ordered after placing order.
                for product in Item.objects.filter(customer=request.user):
                    product.customer.remove(request.user)
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
            # This set of the customer.
            instance.user = request.user
            # This set of the customer Order table.            
            instance.order = customer_order
            # This will make the "ordered" and "in_cart" field equals to True in OrderItem table.
            for product in customer_items:
                product.ordered = True
                product.in_cart = False                
                product.save()
            # Remove all the product that customer ordered after placing order.
            for product in Item.objects.filter(customer=request.user):
                product.customer.remove(request.user)
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
    # The admin has only the access to make the finish_transaction field turns into True.
    payment = Payment.objects.filter(user=request.user, finish_transaction=False).order_by('-id') 
    transaction_completed = Payment.objects.filter(user=request.user, finish_transaction=True).order_by('-id') 
    # If the admin click the "finish_transaction" field check this will turns into to True.    
    if transaction_completed.exists():
        # And all the OrderItem object that has the order of customer will be deleted.
        customer_order_items = transaction_completed.first().order.items.all()
        for data in customer_order_items:
            data.delete()
            
        # Then that Order table will be deleted.
        for data in transaction_completed:
            data.order.delete()

    # If the customer has no order yet.
    if not all_order.exists():
        context = {'customer_exists': all_order.exists(), 'order_quantity': order_quantity(request)}   
        return render(request, 'store/delivery.html', context)              
    
    context = {'all_order': all_order, 'payment': payment, 'order_quantity': order_quantity(request), 'customer_exists': all_order.exists()}
    return render(request, 'store/pending-orders.html', context)
