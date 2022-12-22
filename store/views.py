from .forms import CaffeinatedForm, OnlyWaterForm, PizzaForm, MainForm, DeliveryForm, CollectionForm
from .models import AddOn, Item, FavoriteItem, OrderItem, Order, DeliveryFee, Payment
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.    
def home(request):    
    # This function will delete the OrderItem and Delivery or Collection table.
    if request.user.is_authenticated:
        delete_transactions(request)
    
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
      
# This kind of detail is only for the category of Caffeinated.
def detail_caffeinated(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)                                        
    caffeinated_form = CaffeinatedForm()
    add_on = AddOn.objects.all()
    add_on = add_on.first()
    
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
                    instance.price = item.price
                else:
                    instance.price = item.cold_price
                    
                instance.hot_cold = caffeinated_form.cleaned_data['hot_or_cold']   
                        
                # This will check the checkbox if the customer would like to add an add-ons.
                # Also to add the price and total it.
                if caffeinated_form.cleaned_data['milk']:
                    instance.total_price += add_on.milk
                    instance.milk = True
                if caffeinated_form.cleaned_data['whip_cream']:
                    instance.total_price += add_on.whip_cream
                    instance.whip_cream = True
                if caffeinated_form.cleaned_data['syrup_pump']:
                    instance.total_price += add_on.syrup_pump
                    instance.syrup_pump = True
                if caffeinated_form.cleaned_data['espresso_shot']:
                    instance.espresso_shot = True     
                    instance.total_price += add_on.espresso_shot
                    
                order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)                    
                # If the item is already in the OrderItem table then it will just increase the quantity and the price.                        
                if order_item:                                            
                    # If the the product has only 1 in OrderItem table.
                    if order_item.count() == 1:
                        order_item = order_item.last()
                        # If the customer go back again on the specific product and the customer click again the "Add to Cart" button.
                        # Then it will check first if the customer still wants to buy the same add-ons.
                        # If the customer is, then it will just increment the quantity of this product.
                        if instance.hot_or_cold == order_item.hot_or_cold and order_item.milk == instance.milk and order_item.whip_cream == instance.whip_cream and order_item.syrup_pump == instance.syrup_pump and order_item.espresso_shot == instance.espresso_shot:
                            order_item.quantity += 1
                            order_item.save()
                            return redirect('store:cart')  
                        
                    # If the the product has more than 1 in OrderItem table.    
                    # And has the same add-ons.  
                    else:
                        for data in order_item:
                            if instance.hot_or_cold == data.hot_or_cold and data.milk == instance.milk and data.whip_cream == instance.whip_cream and data.syrup_pump == instance.syrup_pump and data.espresso_shot == instance.espresso_shot:
                                data.quantity += 1
                                data.save()
                                return redirect('store:cart')      
                            
                # This will add the item to OrderItem table and input whatever the customer added.
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)                 
                order.items.add(caffeinated_form.save())  
                instance.total_price += instance.price 
                instance.in_cart = True   
                item.customer.add(request.user)
                item.save()                                              
                instance.save()                  
            return redirect('store:cart')                                                                                                                                 
        else:
            return redirect('account:sign-in')                                              
        
    context = {'item': item, 'caffeinated_form': caffeinated_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context)

# This kind of detail is only for the category of Coolers.
def detail_coolers(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)  
    
    if request.method == 'POST':        
        if request.user.is_authenticated:            
            order_item_filter = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)
            
            # If the item is already in the OrderItem table then it will just increase the quantity and the price.
            if order_item_filter:
                order_item = OrderItem.objects.get(user=request.user, item=item, ordered=False, in_cart=True)
                order_item.quantity += 1
                order_item.total_price += order_item.price                
                order_item.save()
                return redirect('store:cart')                                                                                                                                                                                                                                                                                              
                
            # This will add the item to OrderItem table and input whatever the customer added.                            
            order_item_create = OrderItem.objects.create(user=request.user, item=item, ordered=False, in_cart=True)
            order, created = Order.objects.get_or_create(user=request.user, ordered=False)     
            order.items.add(order_item_create) 
            order_item_create.in_cart = True
            order_item_create.total_price = item.price
            item.customer.add(request.user)  
            item.save()              
            order_item_create.save()                         
            return redirect('store:cart')                                                                                                                                                                                                                                                                                              
        else:
            return redirect('account:sign-in')
                                          
    context = {'item': item, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context)

# This kind of detail is only for those items that its add-ons is only bottled water.
def detail_only_water(request, category, item_slug):
    item = Item.objects.get(category=category, item_slug=item_slug)  
    favorite_list = FavoriteItem.objects.filter(user=request.user, item=item).first()
    in_favorite_list = False    
    
    if favorite_list:
        in_favorite_list = True
        print('Favorite list:', favorite_list)
        
    only_water_form = OnlyWaterForm()
    add_on = AddOn.objects.all()
    add_on = add_on.first()   
    
    if request.method == 'POST':        
        if request.user.is_authenticated:
            only_water_form = OnlyWaterForm(request.POST)
            if only_water_form.is_valid():
                instance = only_water_form.save(commit=False)
                instance.user = request.user
                instance.item = item
                
                # This will check the checkbox if the customer would like to add a bottled water.
                # Also to add the price and total it.
                if only_water_form.cleaned_data['bottled_water']:
                    instance.total_price += add_on.bottled_water
                    instance.bottled_water = True
                                    
                order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)                    
                # If the item is already in the OrderItem table then it will just increase the quantity and the price.                        
                if order_item:                                            
                    # If the the product has only 1 in OrderItem table.
                    if order_item.count() == 1:
                        order_item = order_item.last()
                        # If the customer go back again on the specific product and the customer click again the "Add to Cart" button.
                        # Then it will check first if the customer still wants to buy the same add-ons.
                        # If the customer is, then it will just increment the quantity of this product.
                        if instance.bottled_water == order_item.bottled_water:
                            order_item.quantity += 1
                            order_item.save()
                            return redirect('store:cart')  
                        
                    # If the the product has more than 1 in OrderItem table.             
                    else:
                        for data in order_item:
                            if instance.bottled_water == data.bottled_water:
                                data.quantity += 1
                                data.save()
                                return redirect('store:cart')                                                                                                                                                                                                                                                                                             

                # This will add the item to OrderItem table and input whatever the customer added.                
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)     
                order.items.add(only_water_form.save()) 
                instance.price = item.price
                instance.total_price += instance.price
                instance.in_cart = True                
                item.customer.add(request.user)  
                item.save()              
                instance.save()   
                return redirect('store:cart')                                                                                                                                                                                                                                                                                              
        else:
            return redirect('account:sign-in')
                                          
    context = {'item': item, 'only_water_form': only_water_form, 'add_on': add_on, 'in_favorite_list': in_favorite_list, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context)

def favorite_list(request):
    favorite_item = FavoriteItem.objects.filter(user=request.user)           
    # If the customer has no order yet.    
    if not favorite_item.exists():  
        return no_order_yet(request, 'favorites')         
    
    context = {'favorite_item': favorite_item,'order_quantity': order_quantity(request)}
    return render(request, 'store/favorite-list.html', context)

def add_favorite(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)                                        
    favorite_item = FavoriteItem.objects.create(user=request.user, item=item)
    favorite_item.save()
    return redirect('store:favorite-list')

def remove_favorite(request, item_slug):
    print('Remove favorite:', item_slug)
    return redirect('store:favorite-list')

# This kind of detail is only for the category of Pizza.
def detail_pizza(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)  
    pizza_form = PizzaForm()
    add_on = AddOn.objects.all()
    add_on = add_on.first() 

    if request.method == 'POST':        
        if request.user.is_authenticated:
            pizza_form = PizzaForm(request.POST)
            if pizza_form.is_valid():
                instance = pizza_form.save(commit=False)
                instance.user = request.user
                instance.item = item
                
                # This will check the checkbox if the customer would like to add a bottled water.
                # Also to add the price and total it.
                if pizza_form.cleaned_data['bacon']:
                    instance.total_price += add_on.bacon
                    instance.bacon = True
                if pizza_form.cleaned_data['pepperoni']:
                    instance.total_price += add_on.pepperoni
                    instance.pepperoni = True
                if pizza_form.cleaned_data['ham']:
                    instance.total_price += add_on.ham
                    instance.ham = True
                if pizza_form.cleaned_data['cheese']:
                    instance.total_price += add_on.cheese
                    instance.cheese = True
                                    
                order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)                    
                # If the item is already in the OrderItem table then it will just increase the quantity and the price.                        
                if order_item:                                            
                    # If the the product has only 1 in OrderItem table.
                    if order_item.count() == 1:
                        order_item = order_item.last()
                        # If the customer go back again on the specific product and the customer click again the "Add to Cart" button.
                        # Then it will check first if the customer still wants to buy the same add-ons.
                        # If the customer is, then it will just increment the quantity of this product.
                        if instance.bacon == order_item.bacon and instance.pepperoni == order_item.pepperoni and instance.ham == order_item.ham and instance.cheese == order_item.cheese:
                            order_item.quantity += 1
                            order_item.save()
                            return redirect('store:cart')  
                        
                    # If the the product has more than 1 in OrderItem table.             
                    else:
                        for data in order_item:
                            if instance.bacon == data.bacon and instance.pepperoni == data.pepperoni and instance.ham == data.ham and instance.cheese == data.cheese:
                                data.quantity += 1
                                data.save()
                                return redirect('store:cart')                                                                                                                                                                                                                                                                                             

                # This will add the item to OrderItem table and input whatever the customer added.                
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)     
                order.items.add(pizza_form.save()) 
                instance.price = item.price
                instance.total_price += instance.price
                instance.in_cart = True                
                item.customer.add(request.user)  
                item.save()              
                instance.save()   
                return redirect('store:cart')                                                                                                                                                                                                                                                                                              
        else:
            return redirect('account:sign-in')
    
    context = {'item': item, 'pizza_form': pizza_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context)

# This kind of detail is for the following categories:.
def detail_main(request, item_slug):
    item = Item.objects.get(item_slug=item_slug)  
    main_form = MainForm()
    add_on = AddOn.objects.all()
    add_on = add_on.first() 

    if request.method == 'POST':        
        if request.user.is_authenticated:
            main_form = MainForm(request.POST)
            if main_form.is_valid():
                instance = main_form.save(commit=False)
                instance.user = request.user
                instance.item = item
                
                # This will check the checkbox if the customer would like to add an add-ons.
                # Also to add the price and total it.
                if main_form.cleaned_data['plain_rice']:
                    instance.total_price += add_on.plain_rice
                    instance.plain_rice = True
                if main_form.cleaned_data['rice_platter']:
                    instance.total_price += add_on.rice_platter
                    instance.rice_platter = True
                if main_form.cleaned_data['aligue_platter']:
                    instance.total_price += add_on.aligue_platter
                    instance.aligue_platter = True
                if main_form.cleaned_data['bottled_water']:
                    instance.total_price += add_on.bottled_water
                    instance.bottled_water = True
                                    
                order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False, in_cart=True)                    
                # If the item is already in the OrderItem table then it will just increase the quantity and the price.                        
                if order_item:                                            
                    # If the the product has only 1 in OrderItem table.
                    if order_item.count() == 1:
                        order_item = order_item.last()
                        # If the customer go back again on the specific product and the customer click again the "Add to Cart" button.
                        # Then it will check first if the customer still wants to buy the same add-ons.
                        # If the customer is, then it will just increment the quantity of this product.
                        if instance.plain_rice == order_item.plain_rice and instance.rice_platter == order_item.rice_platter and instance.aligue_platter == order_item.aligue_platter and instance.bottled_water == order_item.bottled_water:                            
                            order_item.quantity += 1
                            order_item.save()
                            return redirect('store:cart')  
                        
                    # If the the product has more than 1 in OrderItem table.             
                    else:
                        for data in order_item:
                            if instance.plain_rice == data.plain_rice and instance.rice_platter == data.rice_platter and instance.aligue_platter == data.aligue_platter and instance.bottled_water == data.bottled_water:
                                data.quantity += 1
                                data.save()
                                return redirect('store:cart')                                                                                                                                                                                                                                                                                             

                # This will add the item to OrderItem table and input whatever the customer added.                
                order, created = Order.objects.get_or_create(user=request.user, ordered=False)     
                order.items.add(main_form.save()) 
                instance.price = item.price
                instance.total_price += instance.price
                instance.in_cart = True                
                item.customer.add(request.user)  
                item.save()              
                instance.save()   
                return redirect('store:cart')                                                                                                                                                                                                                                                                                              
        else:
            return redirect('account:sign-in')
    
    context = {'item': item, 'main_form': main_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-detail.html', context) 

@login_required
def caffeinated_update(request, item_slug, order_item_id):
    item = Item.objects.get(item_slug=item_slug)
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)    
    caffeinated_form = CaffeinatedForm(instance=order_item)
    add_on = AddOn.objects.all()
    add_on = add_on.first()
    
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
                 
            instance.total_price = 0
            # This update among add-ons.
            if caffeinated_form.cleaned_data['milk']:
                instance.total_price += add_on.milk
                instance.milk = True
            if caffeinated_form.cleaned_data['whip_cream']:
                instance.total_price += add_on.whip_cream
                instance.whip_cream = True
            if caffeinated_form.cleaned_data['syrup_pump']:
                instance.total_price += add_on.syrup_pump
                instance.syrup_pump = True
            if caffeinated_form.cleaned_data['espresso_shot']:
                instance.espresso_shot = True     
                instance.total_price += add_on.espresso_shot
                
            # If the item is already in the OrderItem table then it will just increase the quantity and the price.                                                            
            instance.total_price += instance.price                    
            instance.save() 
            
            order_item = OrderItem.objects.filter(user=request.user, item=item, hot_cold=instance.hot_cold, milk=instance.milk, whip_cream=instance.whip_cream, syrup_pump=instance.syrup_pump, espresso_shot=instance.espresso_shot, ordered=False, in_cart=True)                                       
            update_duplicate(request, item, order_item, order_item_id)                                                                                              
                        
        return redirect('store:cart')
    
    context = {'item':item, 'order_item': order_item, 'caffeinated_form': caffeinated_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-update.html', context)

@login_required
def only_water_update(request, category, item_slug, order_item_id):
    item = Item.objects.get(category=category, item_slug=item_slug)
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)    
    only_water_form = OnlyWaterForm(instance=order_item)
    add_on = AddOn.objects.all()
    add_on = add_on.first()

    if request.method == 'POST':
        only_water_form = OnlyWaterForm(request.POST, instance=order_item)
        if only_water_form.is_valid():
            instance = only_water_form.save(commit=False)   

            instance.total_price = 0         
               
            instance.price = item.price            
            # This will check the checkbox if the customer would like to add a bottled water or to remove it.
            # Also to add the price and total it.
            if only_water_form.cleaned_data['bottled_water']:
                instance.total_price += add_on.bottled_water
                instance.bottled_water = True    
                 
            instance.total_price += instance.price                    
            instance.save()     
            
            # This will check if there has duplicate item.  
            order_item = OrderItem.objects.filter(user=request.user, item=item, bottled_water=instance.bottled_water, ordered=False, in_cart=True)                                       
            update_duplicate(request, item, order_item, order_item_id)       
            
        return redirect('store:cart')
        
    context = {'item':item, 'order_item': order_item, 'only_water_form': only_water_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-update.html', context)

@login_required
def pizza_update(request, item_slug, order_item_id):
    item = Item.objects.get(item_slug=item_slug)
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)    
    pizza_form = PizzaForm(instance=order_item)
    add_on = AddOn.objects.all()
    add_on = add_on.first()

    if request.method == 'POST':
        caffeinated_form = PizzaForm(request.POST, instance=order_item)
        if caffeinated_form.is_valid():
            instance = caffeinated_form.save(commit=False)
                  
            instance.price = item.price
                                 
            instance.total_price = 0
            # This update among add-ons.
            if caffeinated_form.cleaned_data['bacon']:
                instance.total_price += add_on.bacon
                instance.bacon = True
            if caffeinated_form.cleaned_data['pepperoni']:
                instance.total_price += add_on.pepperoni
                instance.pepperoni = True
            if caffeinated_form.cleaned_data['ham']:
                instance.total_price += add_on.ham
                instance.ham = True
            if caffeinated_form.cleaned_data['cheese']:
                instance.cheese = True     
                instance.total_price += add_on.cheese
                
            # If the item is already in the OrderItem table then it will just increase the quantity and the price.                                                                                            
            instance.total_price += instance.price                    
            instance.save()    

            # This will check if there has duplicate item.  
            order_item = OrderItem.objects.filter(user=request.user, item=item, plain_rice=instance.plain_rice, rice_platter=instance.rice_platter, aligue_platter=instance.aligue_platter, bottled_water=instance.bottled_water, ordered=False, in_cart=True)                                       
            update_duplicate(request, item, order_item, order_item_id)                                                                       
            
        return redirect('store:cart')

    context = {'item':item, 'order_item': order_item, 'pizza_form': pizza_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
    return render(request, 'store/product-update.html', context)   

@login_required
def main_update(request, item_slug, order_item_id):
    item = Item.objects.get(item_slug=item_slug)
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)    
    main_form = MainForm(instance=order_item)
    add_on = AddOn.objects.all()
    add_on = add_on.first()

    if request.method == 'POST':
        main_form = MainForm(request.POST, instance=order_item)
        if main_form.is_valid():
            instance = main_form.save(commit=False)                  
            instance.price = item.price                                 
            instance.total_price = 0
            # This update among add-ons.
            if main_form.cleaned_data['plain_rice']:
                instance.total_price += add_on.plain_rice
                instance.plain_rice = True
            if main_form.cleaned_data['rice_platter']:
                instance.total_price += add_on.rice_platter
                instance.rice_platter = True
            if main_form.cleaned_data['aligue_platter']:
                instance.total_price += add_on.aligue_platter
                instance.aligue_platter = True
            if main_form.cleaned_data['bottled_water']:
                instance.bottled_water = True     
                instance.total_price += add_on.bottled_water
                
            # If the item is already in the OrderItem table then it will just increase the quantity and the price.                                                                            
            instance.total_price += instance.price                    
            instance.save()            
            
            order_item = OrderItem.objects.filter(user=request.user, item=item, plain_rice=instance.plain_rice, rice_platter=instance.rice_platter, aligue_platter=instance.aligue_platter, bottled_water=instance.bottled_water, ordered=False, in_cart=True)                                       
            update_duplicate(request, item, order_item, order_item_id)                                                      
            
        return redirect('store:cart') 
            
    context = {'item':item, 'order_item': order_item, 'main_form': main_form, 'add_on': add_on, 'order_quantity': order_quantity(request)}
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
    items_category = None    
    coffee_classics = None
    special_latte = None
    frappe = None
    other_drinks = None        
    categorized_items = None        
    
    if item_category == 'Caffeinated':
        coffee_classics = Item.objects.filter(category='Coffee Classics')
        special_latte = Item.objects.filter(category='Special Latte')
        items_category = item_category
    elif item_category == 'Coolers':
        frappe = Item.objects.filter(category='Frappe')
        other_drinks = Item.objects.filter(category='Other Drinks')
        items_category = item_category
    elif item_category == 'Other Drinks':
        other_drinks = Item.objects.filter(category='Other Drinks')
        items_category = item_category
    else:
        categorized_items = Item.objects.filter(category=item_category)
        items_category = categorized_items.first().category

    context = {'categorized_items': categorized_items, 'items_category': items_category, 'coffee_classics': coffee_classics, 'special_latte': special_latte, 'other_drinks': other_drinks, 'frappe': frappe, 'order_quantity': order_quantity(request)}
    return render(request, 'store/specific-category.html', context)    

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, ordered=False)  
    # If the customer has no order yet.
    if not order.exists():
        return no_order_yet(request, 'cart')
    
    customer_order = order.first()    
    all_order = customer_order.items.all().order_by('-id')     
    
    # Delete the customer in Order table if the customer has no order left in cart.
    order_count = customer_order.items.all().count()                      
    if order_count == 0:
        Order.objects.get(user=request.user, ordered=False).delete()
    if all_order.exists():
        context = {'all_order': all_order, 'customer_order': customer_order, 'order_quantity': order_quantity(request), 'sub_total': sub_total(request), 'count_order': order_count}           
        return render(request, 'store/cart.html', context)
    else:
        return no_order_yet(request, 'cart')

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, ordered=False)                
    # If the customer has no order yet.
    if not order.exists():
        return no_order_yet(request, 'checkout') 

    # All the customer order will display on right side navigation.
    all_order = order.first().items.all().order_by('-id') 
    
    context = {'order_quantity': order_quantity(request), 'all_order': all_order, 'customer_exists': order.exists()}
    return render(request, 'store/checkout.html', context)

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
    order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False)    
    order_item_count = OrderItem.objects.filter(user=request.user, item=item, ordered=False).count()    

    # When the order item quantity is zero then delete in order item table.
    # If the customer has only 1 the same product left then delete the Item object in OrderItem Table and remove also the customer to that product. 
    if order_item_count == 1:
        item.customer.remove(request.user)                       
        OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False).delete()
        
    # If not, then remove only the Item in OrderItem table.        
    if order_item_count > 1:
        order_item.delete()
        
    return redirect('store:cart')       

@login_required
def delivery(request):
    order = Order.objects.filter(user=request.user, ordered=False)     
    # If the customer has no order yet.
    if not order.exists():
        return no_order_yet(request, 'delivery')
    
    # If the sum of subtotal is below 300 that is the minimum amount of delivery fee then you cannot proceed to delivery.    
    maximum_delivery_fee = DeliveryFee.objects.all().first().maximum_delivery_fee    
    subtotal = sub_total(request)          
    if subtotal < maximum_delivery_fee:
        messages.error(request, f'Please add your order to make it ₱' + str(maximum_delivery_fee) + ' amount to proceed to delivery. You could also click the collection instead.')              
        return redirect('store:checkout')

    order_items = OrderItem.objects.filter(user=request.user, ordered=False, in_cart=True)     

    # Get the customer orders. Calculate subtotal and total.
    customer_order = order.first() 
    customer_items = order_items.all() 
    
    all_order = customer_order.items.all().order_by('-id')
    
    # About of the total expense.
    districts_delivery_fee = DeliveryFee.objects.all().first()
    delivery_fee = districts_delivery_fee.arevalo 
    total = delivery_fee + sub_total(request)
    
    delivery_form = DeliveryForm()
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)       
        office_home = request.POST.get('home-office') 
        if delivery_form.is_valid():
            instance = delivery_form.save(commit=False)
            # Setting of delivery fee according to the district location.
            district_location = delivery_form.cleaned_data['districts']
            delivery_fee_amount = DeliveryFee.objects.all().first()
            if district_location == 'Arevalo':
                delivery_fee = delivery_fee_amount.arevalo     
            if district_location == 'City Proper':
                delivery_fee = delivery_fee_amount.city_proper
            if district_location == 'Jaro':
                delivery_fee = delivery_fee_amount.jaro
            if district_location == 'La Paz':
                delivery_fee = delivery_fee_amount.la_paz
            if district_location == 'Lapuz':
                delivery_fee = delivery_fee_amount.lapuz
            if district_location == 'Mandurriao':
                delivery_fee = delivery_fee_amount.mandurriao
            if district_location == 'Molo':
                delivery_fee = delivery_fee_amount.molo       
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
                total = delivery_fee + sub_total(request)                                    
                customer_order.save()
                instance.save()
                Payment.objects.create(user=request.user, delivery=delivery_form.instance, order=customer_order, subtotal=subtotal, delivery_fee=delivery_fee, total=total)  
                return redirect('store:thank-you') 
            else:
                messages.error(request, 'Please select a label between office or home')      

    context = {'delivery_form': delivery_form, 'delivery_fee': delivery_fee, 'districts_delivery_fee': districts_delivery_fee, 'all_order': all_order, 'sub_total': sub_total(request), 'total': total, 'order_quantity': order_quantity(request), 'customer_exists': order.exists()}
    return render(request, 'store/delivery.html', context)

@login_required
def collection(request):    
    order = Order.objects.filter(user=request.user, ordered=False)     
    # If the customer has no order yet.
    if not order.exists():
        return no_order_yet(request, 'collection')

    # Get the customer orders. Calculate subtotal and total.    
    # The subtotal and total is the same due to had no delivery fee charge.
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)     
    customer_order = order.first()           
    customer_items = order_items.all()   
    all_order = customer_order.items.all().order_by('-id') 
    total = sub_total(request)

    collection_form = CollectionForm()    
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

    context = {'collection_form': collection_form, 'all_order': all_order, 'total': sub_total(request), 'order_quantity': order_quantity(request), 'customer_exists': order.exists()}
    return render(request, 'store/collection.html', context)

# After you place your order.
@login_required
def thank_you(request):
    return render(request, 'store/thank-you.html')    

# This where your pending orders show.
@login_required
def pending_orders(request):
    # This will get all what you ordered and display the information that you input.    
    all_order = Order.objects.filter(user=request.user, ordered=True).order_by('-id')  
    # If the customer has no order yet.
    if not all_order.exists():
        return no_order_yet(request, 'pending orders') 
     
    add_on = AddOn.objects.all()
    add_on = add_on.first()    
  
    # The pending orders will appear as long as you don't claim or we didn't delivered yet.
    # The admin has only the access to make the finish_transaction field turns into True.
    payment = Payment.objects.filter(user=request.user, finish_transaction=False).order_by('-id') 
    
    # This function will delete the OrderItem and Delivery or Collection table.    
    delete_transactions(request)           
    
    context = {'all_order': all_order, 'payment': payment, 'add_on': add_on, 'order_quantity': order_quantity(request), 'customer_exists': all_order.exists()}
    return render(request, 'store/pending-orders.html', context)

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

# This function is for an update item when there is already has the same item and add ons then it will be deleted one of them and add the quantity to the single item.
def update_duplicate(request, item,  order_item, order_item_id):
    if order_item.count() > 1:
        for data in order_item:                   
            if data.id != order_item_id:
                duplicate_order_item = OrderItem.objects.get(id=data.id, user=request.user, item=item, ordered=False, in_cart=True)                                       
                current_order_item = OrderItem.objects.get(id=order_item_id, user=request.user, item=item, ordered=False, in_cart=True)                                                                                    
                
                # When the item quantity is more than the quantity of its duplicate then delete the other duplicate and add the quantity of that dupilcate.
                if current_order_item.quantity > duplicate_order_item.quantity:
                    current_order_item.quantity += duplicate_order_item.quantity
                    current_order_item.save()
                    duplicate_order_item.delete()                            
                    return redirect('store:cart')
                                     
                duplicate_order_item.quantity += current_order_item.quantity
                duplicate_order_item.save()     
                current_order_item.delete()          

# This function will delete all the OrderItem, Delivery or Collection if the customer transaction is finish.
def delete_transactions(request):
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

# This function will display the page if the customer has no order yet.
def no_order_yet(request, page_header_title):   
    # If the customer has no order yet.
    context = {'page_header_title': page_header_title, 'order_quantity': order_quantity(request)}   
    return render(request, 'store/order-first.html', context) 