import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}


    items = []
    order = {'total_quantity': 0, 'total_cart': 0, 'shipping': False}
    cartItems = order['total_quantity']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            if product.offer:
                total = (product.offer * cart[i]['quantity'])
            else:
                total = (product.price * cart[i]['quantity'])

            order['total_cart'] += total
            order['total_quantity'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'offer': product.offer,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'total_price': total
            }
            items.append(item)

            if product.ship == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}



