
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Grocery product details
PRODUCTS = [
    {
        'id': 1,
        'name': 'Fresh Tomatoes',
        'price': 40,
        'image': 'tomatoes.jpg',
        'description': 'Fresh and organic tomatoes'
    },
    {
        'id': 2,
        'name': 'Fresh Apples',
        'price': 120,
        'image': 'apples.jpg',
        'description': 'Sweet and fresh apples'
    },
    {
        'id': 3,
        'name': 'Fresh Milk',
        'price': 60,
        'image': 'milk.jpg',
        'description': 'Pure and healthy milk'
    },
    {
        'id': 4,
        'name': 'Potatoes',
        'price': 35,
        'image': 'potatoes.jpg',
        'description': 'Fresh farm potatoes'
    },
    {
        'id': 5,
        'name': 'Fresh Bananas',
        'price': 50,
        'image': 'bananas.jpg',
        'description': 'Fresh ripe bananas'
    },
    {
        'id': 6,
        'name': 'Rice',
        'price': 80,
        'image': 'rice.jpg',
        'description': 'Quality everyday rice'
    },
]


# Home page
def home(request):
    return render(request, 'home.html', {
        'products': PRODUCTS
    })


# Products page
def products(request):
    return render(request, 'products.html', {
        'products': PRODUCTS
    })


# Product details page
def product_detail(request, product_id):

    product = next(
        (p for p in PRODUCTS if p['id'] == product_id),
        None
    )

    if product is None:
        return render(
            request,
            'product_not_found.html',
            status=404
        )

    return render(request, 'product_detail.html', {
        'product': product
    })


# Add product to cart
def add_to_cart(request, product_id):

    if request.method == 'POST':

        product = next(
            (p for p in PRODUCTS if p['id'] == product_id),
            None
        )

        if product:
            cart_data = request.session.get('cart', {})
            product_key = str(product_id)

            cart_data[product_key] = (
                cart_data.get(product_key, 0) + 1
            )

            request.session['cart'] = cart_data
            request.session.modified = True

            messages.success(
                request,
                'Product added to cart successfully!'
            )

    return redirect('cart')


# Shopping cart
def cart(request):

    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = next(
            (p for p in PRODUCTS if p['id'] == int(product_id)),
            None
        )

        if product:
            item = product.copy()
            item['quantity'] = quantity
            item['subtotal'] = item['price'] * quantity

            cart_items.append(item)
            total += item['subtotal']

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# Remove product from cart
def remove_from_cart(request, product_id):

    if request.method == 'POST':

        cart_data = request.session.get('cart', {})
        cart_data.pop(str(product_id), None)

        request.session['cart'] = cart_data
        request.session.modified = True

    return redirect('cart')


# Login page
def login_view(request):

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
                'Login successful!'
            )

            return redirect('home')

        else:
            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(request, 'login.html')


# Registration page
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([
            username, email, password, confirm_password
        ]):
            messages.error(
                request,
                'Please fill in all fields.'
            )

        elif password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )

        elif User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username already exists.'
            )

        elif User.objects.filter(email=email).exists():
            messages.error(
                request,
                'Email already registered.'
            )

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                'Registration successful! Please login.'
            )

            return redirect('login')

    return render(request, 'register.html')


# Logout
def logout_view(request):

    if request.method == 'POST':
        logout(request)

    return redirect('home')
