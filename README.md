
# Cafe_Riama

## Description
Cafe_Riama is an e-commerce website where you can choose 12 types of products. Cafe Riama is located in Iloilo City, Philippines.

- I build this project to solve the many time's problems Cafe Riama coffee shop encountered.
- This solves the problem of the shop where customers always tell the staff that they don't order the given items. Now, there are no reasons anymore because they have their listed orders and the information that the customer input before they will place their orders.
- I learned how to query and use the database more and somehow how to use function as a reusable code.

## Built With
- HTML
- CSS
- JavaScript (ES6)
- Bootstrap (5.1)
- Django (4.0.6)

## How to Install and Run the Project

Install the Cafe_Riama with the following:

```bash
  pip install -r requirements.txt
  python manage.py runserver
```

## How to Use the Project
#### You sign up.
![sign up](screenshots/sign-up.png?raw=true)
#### Then sign in.
![sign in](screenshots/sign-in.png?raw=true)
#### You can still visit the page, even though you did not have an account. If you notice on the navbar, it added the following buttons: Cart, Pendings, Favorites, Profile and SignOut.
![home1](screenshots/home1.png?raw=true)
![home2](screenshots/home2.png?raw=true)
![home3](screenshots/home3.png?raw=true)
![home4](screenshots/home4.png?raw=true)
![home5](screenshots/home5.png?raw=true)
#### Let's say you click the cappuccino. Now you can choose your options and add-ons to it. Click add to cart button when you are finished. Remember, you will be redirected to the sign-in page if you don't sign in yet and you just click the add to cart button.
![caffeinated detail](screenshots/caffeinated-detail.png?raw=true)
#### There is now your order item. You can click the up and down button to increase or decrease your item quantity. You could also remove it.
![cart1](screenshots/cart1.png?raw=true) 
#### In the Categories dropdown, there is a list of categories of items. The All Products dropdown item displays all the categories of items.
![cart2](screenshots/cart2.png?raw=true)
#### Click the buttons to help you navigate instantly for your desired food and drink. The blue border on the cappuccino indicates that you already order that and you could also order again.
![all display category 1](screenshots/all-display-category1.png?raw=true)
#### We will choose here is the ham & cheese.
![all display category 2](screenshots/all-display-category2.png?raw=true)
#### Let's just click the add to cart again to order this item.
![pizza detail](screenshots/pizza-detail.png?raw=true)
#### Now, if you want to update the item then click the name of it. The "Ham & Cheese".
![cart 3](screenshots/cart3.png?raw=true)
#### Notice the name of the color blue button becomes "UPDATE".
![pizza update](screenshots/pizza-update.png?raw=true)
#### The price of the Ham & Cheese increases due to your add-ons on it after you update.
![cart 4](screenshots/cart4.png?raw=true)
#### When you add the quantity of Ham & Cheese it will also increase the price and the subtotal accordingly. Click the continue to checkout the blue button.
![cart 5](screenshots/cart5.png?raw=true)
#### You have two options on how you want to get your order. Whether it is delivery or collection. Click the Edit link on the right side if you want to update or if there is something you missed out.
![continue to checkout](screenshots/checkout.png?raw=true)
#### The collection process is you will be the one to collect your order from their store. This is your collection field. Click the blue button to place your order.
![collection](screenshots/collection.png?raw=true)
#### Delivery will deliver them to you only around Iloilo City. There are your delivery fields. Input correctly your district location and choose between labels.
![delivery1](screenshots/delivery1.png?raw=true)
#### Click the blue button to place your order. Remember, your delivery fee is based on where your district is located.
![delivery2](screenshots/delivery2.png?raw=true)
#### This will appear after you place your order and then it will disappear after 1.5 seconds.
![thank-you](screenshots/thank-you.png?raw=true)
#### This is what it looks like for your pending orders. It displays all the information that you input. The admin will make the finish_transaction field turns into True if the transaction is finished, then all the items that were in the Payment table will be deleted.
![pending-orders](screenshots/pending-orders.png?raw=true)

## Acknowledgment
  ### My design was inspired by the following:
- [themeforest.net](https://themeforest.net/item/drexel-psd-ecommerce-templates/screenshots/20031300?index=2) 
- [bootstrapious.com](https://bootstrapious.com/p/bootstrap-footer-bottom) 
- [ikea.com](https://www.ikea.com/gb/en/shoppingcart/) 

## Badges
![open source](https://img.shields.io/badge/Open%20Source-%F0%9F%92%9A-white)
![GitHub contributors](https://img.shields.io/github/contributors/Llanz-dev/Cafe_Riama)
![downloads](https://img.shields.io/github/downloads/Llanz-dev/Cafe_Riama/total)
![Django](https://img.shields.io/badge/django-4.1.1-brightgreen)
![forks](https://img.shields.io/github/last-commit/Llanz-dev/Cafe_Riama)
![followers](https://img.shields.io/github/followers/Llanz-dev?style=social)
![stars](https://img.shields.io/github/stars/Llanz-dev?style=social)
![forks](https://img.shields.io/github/forks/Llanz-dev/Cafe_Riama?style=social)
