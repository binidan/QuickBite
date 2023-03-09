from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Category, Food
from django.db.models import Q
from .forms import MyUserCreationForm, AddressForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Food, Order, Item, Address
from django.contrib import messages
import json

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    foods = Food.objects.filter(
        Q(name__icontains=q) |
        Q(category__name__icontains=q) |
        Q(description__icontains=q)
    )
    categories = Category.objects.all()[0:5]
    context = {
                'categories':categories,
                'foods':foods
              }
    return render(request, 'base/home.html', context)


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
    address_form = AddressForm()
    if request.method == 'POST':
        Address.objects.create(
            customer=request.user,
            country=request.POST.get('country'),
            state=request.POST.get('state'),
            city=request.POST.get('city'),
            street=request.POST.get('street'),
            pincode=request.POST.get('pincode')
        )
        return redirect('checkout')
    context = {
        'address_form':address_form
    }
    return render(request, 'base/address_register.html', context)


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
    elif action == 'remove':
        item.quantity = item.quantity - 1
    item.save()

    if item.quantity <= 0:
        item.delete()

    response_data = {
        'price':item.item_price,
        'quantity': item.quantity
    }

    return JsonResponse(response_data, safe=False)


def cartPage(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            order = Order.objects.get(customer=customer, complete=False)
            items = order.item_set.all()

        except Order.DoesNotExist:
            order = None
            items = None
    order_exists = Order.objects.filter(customer=request.user, complete=False).exists()
    context = {
        'items':items,
        'order':order,
        'order_exists':order_exists
    }

    return render(request, 'base/cart.html', context)


def checkOutPage(request):
    addresses = Address.objects.filter(customer=request.user)
    if request.user.is_authenticated:
        customer = request.user
        try:
            order = Order.objects.get(customer=customer, complete=False)
            items = order.item_set.all()

        except Order.DoesNotExist:
            order = None
            items = None
    
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        selected_address = Address.objects.get(pk=selected_address_id)
        order.address = selected_address
        order.complete = True
        order.save()
        messages.success(request, 'Order has been placed successfully!')
        return redirect('home')

    address_exists = Address.objects.filter(customer=request.user).exists()
    order_exists = Order.objects.filter(customer=request.user, complete=False).exists()

    context = {
        'order_exists':order_exists,
        'address_exists':address_exists,
        'items':items,
        'order':order, 
        'addresses':addresses
        }

    return render(request, 'base/checkout.html', context)


def orderPage(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user, complete=True)
        
        order_exists = Order.objects.filter(customer=request.user, complete=True).exists()
        context = {
            'orders': orders,
            'order_exists': order_exists,
        }
    return render(request, 'base/order.html', context)