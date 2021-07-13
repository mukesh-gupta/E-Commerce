from django.shortcuts import render,get_object_or_404,redirect
from .models import Customer,Order,OrderItem,AddressShip,Product
from django.http import HttpResponse
from .utils import cookieCart
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages
from UserMart.decorators import allowed_users
from .forms import CustomerForm

import json
import datetime

# Create your views here.
@allowed_users(allowed_roles=['customer'])
def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.total_quantity
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    vegitables = Product.objects.filter(category='V')
    fruits=Product.objects.filter(category='F')

    paginator = Paginator(vegitables, 3)
    paginator1 = Paginator(fruits, 3)
    page = request.GET.get('page',1)
    page1 = request.GET.get('page1', 1)
    vegitables_products = paginator.page(page)
    fruits_products = paginator1.page(page1)
    context={
        'cartItems':cartItems,'fruits':fruits_products,'vegitables':vegitables_products
    }
    return render(request,'index.html',context)


@allowed_users(allowed_roles=['customer'])
def ShopCart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.total_quantity

    else:
        cookieData=cookieCart(request)
        order=cookieData['order']
        cartItems=cookieData['cartItems']
        items=cookieData['items']

    context={
        'order': order,'items':items,'cartItems':cartItems
    }
    return render(request,'shoping-cart.html',context)


@allowed_users(allowed_roles=['customer'])
def CartCheckout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.total_quantity
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        items = cookieData['items']
    context={
        'order': order,'items':items,'cartItems':cartItems
    }
    return render(request,'checkout.html',context)



@allowed_users(allowed_roles=['customer'])
def CartDetail(request,pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        items = order.orderitem_set.all()
        cartItems = order.total_quantity

    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        items = cookieData['items']

    products=Product.objects.all()
    item = get_object_or_404(Product, pk=pk)

    context={
        'products':products,'order':order,'items':items,'cartItems':cartItems,'item':item,
    }
    return render(request,'shop-details.html',context)



@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        itemId=data['item']
        action = data['act']
        print('itemId',itemId)
        print('action:',action)

        customer=request.user.customer
        product=Product.objects.get(id=itemId)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if action == 'delete':
            orderItem.quantity >= 0
            orderItem.delete()

        if orderItem.quantity <= 0:
            orderItem.delete()
        return JsonResponse('Item wa added',safe=False)
    else:
        return HttpResponse("You dont't have access to this page")


@allowed_users(allowed_roles=['customer'])
def processOrder(request):
    if request.method == 'POST':
        trans_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

        else:

            print('user is not logged in')

            print('COOKIES:', request.COOKIES)
            name = data['form']['name']
            email = data['form']['email']

            cookieData = cookieCart(request)
            items = cookieData['items']

            customer, created = Customer.objects.get_or_create(
                email=email,
            )
            customer.name = name
            customer.save()

            order = Order.objects.create(
                customer=customer,
                complete=False,
            )

            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                orderItem = OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=item['quantity'],
                )

        total = float(data['form']['total'])
        order.trans_id = trans_id

        if total == float(order.total_cart):
            order.complete = True
        order.save()

        if order.shipping == True:
            AddressShip.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
        return JsonResponse('Payment submitted..', safe=False)
    else:
        return HttpResponse("You dont't have access to this page")


@allowed_users(allowed_roles=['customer'])
def search(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.total_quantity
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Product.objects.all()

    if 'name' in request.POST:
        name = request.POST['name']
        if name:
            products = products.filter(name__icontains=name)

    context = {
        'products': products,'cartItems':cartItems, 'value': request.POST,
    }
    return render(request,'search.html',context)


@allowed_users(allowed_roles=['customer'])
def AccountInfo(request):
    if request.user.is_authenticated:
        user = request.user.customer
        form = CustomerForm(request.POST or None, request.FILES or None,instance=user)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.info(request,"User profile updated successfully !")
                return redirect('setting')
        context={
            'form':form,

        }
        return render(request,'account.html',context)
    else:
        return HttpResponse("you dont't have access to this page")



