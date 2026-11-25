
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from .cart import Cart


def home(request):

    featured_products = Product.objects.filter(
        is_featured=True
    )[:5]

    latest_products = Product.objects.all().order_by(
        '-created_at'
    )[:8]

    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products
    })


def plants(request):

    products = Product.objects.all().order_by(
        '-created_at'
    )

    return render(request, 'store/plants.html', {
        'products': products
    })


def about(request):

    return render(request, 'store/about.html')


def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            messages.success(
                request,
                "Thank you! Your message has been received."
            )

            return redirect('contact')

        messages.error(
            request,
            "Please fill in all fields."
        )

    return render(request, 'store/contact.html')


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.add(product)

    messages.success(
        request,
        f"{product.title} added to your cart!"
    )

    return redirect('plants')


def cart_view(request):

    cart = Cart(request)

    return render(request, 'store/cart.html', {
        'cart': cart
    })


def remove_from_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.remove(product)

    messages.success(
        request,
        "Plant removed from cart."
    )

    return redirect('cart')


def update_cart(request, product_id):

    if request.method == 'POST':

        product = get_object_or_404(
            Product,
            id=product_id
        )

        quantity = int(
            request.POST.get('quantity', 1)
        )

        cart = Cart(request)

        if quantity > 0:
            cart.update(product, quantity)

        else:
            cart.remove(product)

    return redirect('cart')



def signin(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Welcome back to PLANTAE!"
            )

            return redirect('home')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, 'store/signin.html')


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm(request.POST or None)

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    if request.method == 'POST' and form.is_valid():

        user = form.save()
        login(request, user)

        messages.success(
            request,
            "Your PLANTAE account has been created."
        )

        return redirect('home')

    return render(request, 'store/signup.html', {
        'form': form
    })


def signout(request):

    if request.method == 'POST':

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

    return redirect('home')
