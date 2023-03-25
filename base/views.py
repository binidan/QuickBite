from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Category, Food
from django.db.models import Q
from .forms import MyUserCreationForm, AddressForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Food, Item, Address, Order
from django.contrib import messages
import json

# Create your views here.
def home(request):
    categories_all = Category.objects.all()
    foods_recent = Food.objects.all()[0:5]
    foods_discount = Food.objects.order_by('discount')[0:5]
    foods_all = Food.objects.all()
    context = {
                'categories_all':categories_all,
                'foods_recent':foods_recent,
                'foods_discount':foods_discount,
                'foods_all':foods_all
              }
    return render(request, 'base/home_new.html', context)


def shop(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    price_range = request.GET.get('price_range') if request.GET.get('price_range') != None else ''
    min_price, max_price = price_range.split('-') if price_range else (0, 100000)
    foods = Food.objects.filter(
        Q(name__icontains=q) |
        Q(category__title__icontains=q) |
        Q(description__icontains=q),
        Q(price__gte=min_price, price__lte=max_price)
    )

    context = {
        'foods':foods
    }
    return render(request, 'base/shop.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = Customer.object.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username and password does not match")

    return render(request, 'base/login_register.html', {'page':page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form':form})

def userProfile(request, pk):
    pass

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated successfully!')
            return redirect('home')
    return render(request, 'base/update_user.html', {'form':form})

def addressRegister(request):

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = request.user
            address.save()
            return redirect('checkout')
    else:
        address_form = AddressForm()
    context = {
        'address_form':address_form
    }
    return render(request, 'base/checkout_new.html', context)


def updateItem(request):
    data = json.loads(request.body.decode("utf-8"))
    foodId = data['foodId']
    action = data['action']

    customer = request.user
    food = Food.objects.get(id=foodId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    item, created = Item.objects.get_or_create(order=order, food=food)
    if action == 'add':
        item.quantity = item.quantity + 1
    elif action == 'remove' and item.quantity > 1:
        item.quantity = item.quantity - 1
    elif action == 'delete':
        item.quantity = 0
    item.save()

    if item.quantity <= 0:
        item.delete()

    count = order.item_set.all().count()

    response_data = {
        'order_price':order.order_price,
        'total_price':order.total_price,
        'price':item.item_price,
        'quantity': item.quantity,
        'count':count
    }

    return JsonResponse(response_data, safe=False)


def cartPage(request):
    items = None
    order = None
    if request.user.is_authenticated:
        customer = request.user
        try:
            order = Order.objects.get(customer=customer, complete=False)
            items = order.item_set.all()

        except Order.DoesNotExist:
            pass
    order_exists = Order.objects.filter(customer=request.user, complete=False).exists()
    context = {
        'items':items,
        'order':order,
        'order_exists':order_exists
    }

    return render(request, 'base/cart_new.html', context)


def checkOutPage(request):
    order = None
    items = None   
    addresses = None
    address_form = AddressForm()
    if request.user.is_authenticated:      
        customer = request.user
        addresses = Address.objects.filter(customer=customer)
        order = Order.objects.get(customer=customer, complete=False)
        items = order.item_set.all()
        if not order:
            order = Order.objects.create(customer=customer, complete=False)
    
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        selected_address = Address.objects.get(pk=selected_address_id)
        if order is not None:
            order.address = selected_address
            order.complete = True
            order.save()
            messages.success(request, 'Order has been placed successfully!')
            return redirect('home')
        else:
            # Handle the case where an Order object does not exist
            messages.error(request, 'You do not have any pending orders.')
            return redirect('checkout')

    address_exists = Address.objects.filter(customer=request.user).exists()
    order_exists = Order.objects.filter(customer=request.user, complete=False).exists()

    context = {
        'order_exists':order_exists,
        'address_exists':address_exists,
        'items':items,
        'order':order, 
        'addresses':addresses,
        'address_form':address_form
        }

    return render(request, 'base/checkout_new.html', context)


def orderPage(request):
    orders = None
    order_exists = False
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user, complete=True)
        
        order_exists = Order.objects.filter(customer=request.user, complete=True).exists()
    context = {
        'orders': orders,
        'order_exists': order_exists,
    }
    return render(request, 'base/order.html', context)