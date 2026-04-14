from itertools import product
from multiprocessing import context
from django.db import models
from django.db.models import Q, Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from urllib3 import request
from .models import Product, Review,ReviewForm, Category
from .models import Order
from .models import Festival
from .models import ProductImage
from .models import Wishlist
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Cart
import razorpay
from itertools import product as cartesian_product
from django.db.models import Avg, Count

from django.contrib import messages
from django.shortcuts import redirect

from django.shortcuts import render
from django.db.models import Q
from .models import Product
from django.shortcuts import render
from .models import Category


  

from django.http import JsonResponse


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SahoPlusMembership

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserAddress
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests

def chatbot(request):
    return render(request, "bot.html")

        
def chatbot(request):
        return render(request, "bot.html")

def chatbot_view(request):
    return render(request, "bot.html")
 
@login_required
def payment_options_view(request):
    if request.method == 'POST':
        # Here you would securely parse card_number, name_on_card etc.
        pass
    return render(request, 'payment_options.html')

@login_required
def profile_edit_view(request):
    # Ensure the user has a profile object
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Grab standard string data
        profile.display_name = request.POST.get('display_name', '')
        profile.bio = request.POST.get('bio', '')
        profile.gender = request.POST.get('gender', '')
        
        # Handle Date of Birth (Optional field)
        dob = request.POST.get('date_of_birth')
        if dob:
            profile.date_of_birth = dob
            
        # Handle Image File Uploads
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()
        return redirect('profile_edit')  # Refresh page to show changes

    context = {
        'user_profile': profile
    }
    return render(request, 'profile.html', context)

@login_required
def contact_view(request):
    if request.method == 'POST':
        # Here you would process the message: request.POST.get('message')
        pass
    return render(request, 'contact.html')

@login_required
def addresses_view(request):
    # 1. If the user submits the form to add a new address
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        
        # Checkbox returns 'on' if checked, otherwise None
        is_default = request.POST.get('is_default') == 'on'

        # Create and save the new address to the DB
        UserAddress.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=is_default
        )
        
        # Refresh the page so the new address shows up
        return redirect('addresses')

    # 2. Grab all addresses for this user from the database
    saved_addresses = UserAddress.objects.filter(user=request.user).order_by('-is_default')

    # 3. Pass them to the HTML template
    context = {
        'saved_addresses': saved_addresses
    }
    return render(request, 'addresses.html', context)


@login_required
def saho_plus_view(request):
    # Get or create a membership profile for the user
    membership, created = SahoPlusMembership.objects.get_or_create(user=request.user)
    
    context = {
        'membership': membership,
    }
    
    return render(request, 'saho_plus.html', context)



@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.delete()  # remove if already exists

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def add_to_cart(request, product_id):
    if request.method == "POST":
        
        # 🛒 Example cart logic (session-based)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart

        return JsonResponse({
            "status": "success",
            "message": "Product added"
        })

    return JsonResponse({"status": "error"}, status=400)
    

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')   # redirects to home page
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

@login_required
def home_view(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})

def user_logout(request):
    logout(request)  # This clears the session
    return redirect('home')  # Redirect back to homepage
 
from .models import Product
def festival_detail(request, festival_id):
    festival = get_object_or_404(Festival, id=festival_id)
    products = festival.products.all()
    return render(request, 'festival_detail.html', {
        'festival': festival,
        'products': products
    })

def festival_list(request):
    festivals = Festival.objects.all()
    return render(request, 'festival_list.html', {'festivals': festivals})

def fashion_page(request):
    # Get the Category instance
    category_obj = get_object_or_404(Category, name="Fashion")
    
    # Get all subcategories under Fashion
    subcategories = SubCategory.objects.filter(parent_category=category_obj)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "fashion.html", {
        "category": category_obj,
        "subcategories": subcategories,
        "products": products,
    })


def home_decor(request):
    # Get the Category instance
    category = get_object_or_404(Category, slug="home-decor")
    
    # Get all subcategories under Home Decor
    subcategories = SubCategory.objects.filter(parent_category=category)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "homedecor.html", {
        "category": category,
        "subcategories": subcategories,
        "products": products,
    })

from django.shortcuts import get_object_or_404, render
from .models import Product, SubCategory, Category

def electronics(request):
    # Get the Category instance
    category_obj = get_object_or_404(Category, name="Electronics")
    
    # Get all subcategories under Electronics
    subcategories = SubCategory.objects.filter(parent_category=category_obj)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "electronics.html", {
        "category": category_obj,
        "subcategories": subcategories,
        "products": products,
    })

def mobile(request):
    # Get the Category instance
    category_obj = get_object_or_404(Category, name="Mobile")
    
    # Get all subcategories under Mobile
    subcategories = SubCategory.objects.filter(parent_category=category_obj)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "mobile.html", {
        "category": category_obj,
        "subcategories": subcategories,
        "products": products,
    })



def healthcare(request):
    # Get the Category instance
    category_obj = get_object_or_404(Category, name="Healthcare")
    
    # Get all subcategories under Healthcare
    subcategories = SubCategory.objects.filter(parent_category=category_obj)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "healthcare.html", {
        "category": category_obj,
        "subcategories": subcategories,
        "products": products,
    })

def grocery(request):
    # Get the Category instance
    category_obj = get_object_or_404(Category, name="Grocery")
    
    # Get all subcategories under Grocery
    subcategories = SubCategory.objects.filter(parent_category=category_obj)
    
    # Get all products belonging to those subcategories
    products = Product.objects.filter(sub_category__in=subcategories)
    
    return render(request, "grocery.html", {
        "category": category_obj,
        "subcategories": subcategories,
        "products": products,
    })

def about(request):
    return render(request, 'about.html')


def live_search(request):
    query = request.GET.get('q')
    data = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:6]

        for product in products:
            data.append({
                "id": product.id,
                "name": product.name,
                "image": product.image.url
            })

    return JsonResponse(data, safe=False)

def account_view(request):
    return render(request, 'account.html')

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


def settings_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        password = request.POST.get("password")
        if password:
            user.password = make_password(password)
        user.save()
        return redirect("account")  # back to account page
    return render(request, "settings.html")


from django.shortcuts import render, get_object_or_404
from .models import Product

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from .models import Product

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.original_price and product.original_price > product.price:
        product.discount_percentage = round(
            ((product.original_price - product.price) / product.original_price) * 100
        )
    else:
        product.discount_percentage = 0
    reviews = product.reviews.filter(is_approved=True)

    # ⭐ ratings
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    review_count = reviews.count()

    form = ReviewForm()

    # ⭐ breakdown
    rating_breakdown = reviews.values("rating").annotate(count=Count("rating"))
    rating_dict = {i: 0 for i in range(1, 6)}
    for item in rating_breakdown:
        rating_dict[item["rating"]] = item["count"]

    rating_percent = {}
    for i in range(1, 6):
        count = rating_dict.get(i, 0)
        rating_percent[i] = (count / review_count * 100) if review_count > 0 else 0

    # ⭐ review submit
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                existing_review = Review.objects.filter(
                    product=product,
                    user=request.user
                ).first()

                if existing_review:
                    existing_review.rating = form.cleaned_data["rating"]
                    existing_review.comment = form.cleaned_data["comment"]
                    existing_review.save()
                    messages.success(request, "Review updated successfully!")
                else:
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    return redirect("product_details", pk=pk)
        else:
            return redirect("login")

    # ⭐ related products (fixed)
    related_products = Product.objects.filter(
        sub_category__parent_category=product.sub_category.parent_category,
        is_active=True
    ).exclude(id=product.id)[:5]

    context = {
        "product": product,
        "reviews": reviews,
        "rating_dict": rating_dict,
        "rating_percent": rating_percent,
        "form": form,
        "avg_rating": avg_rating,
        "review_count": review_count,
        "related_products": related_products,
        "subcategory": product.sub_category,
        "category": product.sub_category.parent_category,
    }

    return render(request, "product_details.html", context)

# views.py
from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product

def home(request):
    # Show only a few products per category (e.g., 4 each)
    mobile = Product.objects.filter(
    sub_category__parent_category__name="Mobile",
    is_active=True)[:5]
    electronics = Product.objects.filter(
    sub_category__parent_category__name="Electronics",
    is_active=True)[:5]
    fashion = Product.objects.filter(
    sub_category__parent_category__name="Fashion",
    is_active=True)[:5]
    grocery = Product.objects.filter(
    sub_category__parent_category__name="Grocery",
    is_active=True)[:5]
    healthcare = Product.objects.filter(
    sub_category__parent_category__name="Healthcare",
    is_active=True)[:5]
    home_decor = Product.objects.filter(
    sub_category__parent_category__name="Home decor",
    is_active=True)[:5]



    products = Product.objects.filter(is_active=True).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.all())
    )
    hero_products = Product.objects.filter(is_active=True)[:5]
    context = {
        "mobile": mobile,
        "electronics": electronics,
        "fashion": fashion,
        "grocery": grocery,
        "healthcare": healthcare,
        "home_decor": home_decor,
        "products": products,
        "hero_products": hero_products,
    }
    return render(request, 'home.html', {"products": products, **context})

    

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'cart.html',context)

def checkout(request):
    return render(request, 'checkout.html')

def increase_qty(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_qty(request, item_id):
    cart_item = Cart.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

from django.conf import settings

def payment_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    
    print("KEY ID:", settings.RAZORPAY_KEY_ID, type(settings.RAZORPAY_KEY_ID))
    print("KEY SECRET:", settings.RAZORPAY_KEY_SECRET, type(settings.RAZORPAY_KEY_SECRET))

    order_amount = int(product.price * 100)  # in paise
    order_currency = 'INR'
    order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture='1'))

    context = {
        "product": product,
        "order_id": order['id'],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": order_amount,
    }
    return render(request, "payment.html", context)

    # views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_failed(request):
    return render(request, "failed.html")

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
            # ✅ Signature is valid — mark order as paid
            return render(request, "success.html")
        except razorpay.errors.SignatureVerificationError:
            # ❌ Signature mismatch — possible fraud
            return HttpResponseBadRequest("Payment verification failed")
    return HttpResponseBadRequest("Invalid request")

def category_page(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'category.html', {'products': products})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    subcategory_products = {}
    for sub in subcategories:
        products = sub.products.all()
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if sort == "price_asc":
            products = products.order_by("price")
        elif sort == "price_desc":
            products = products.order_by("-price")
        elif sort == "newest":
            products = products.order_by("-id")  # assuming id ~ newest
        elif sort == "rating":
            products = products.order_by("-rating")

        subcategory_products[sub] = products

    # AJAX partial response
    if request.GET.get("ajax"):
        return render(request, "your_app/product_grid.html", {
            "subcategory_products": subcategory_products
        })

    return render(request, "your_app/category_details.html", {
        "category": category,
        "subcategory_products": subcategory_products
    })

def product_list(request):
    categories = Category.objects.prefetch_related("subcategories__products").all()
    return render(request, "your_app/products.html", {"categories": categories})


def fashion_view(request):
    # Get the main Fashion category
    fashion_category = get_object_or_404(Category, name="Fashion")

    # Get all subcategories under Fashion
    subcategories = fashion_category.subcategories.all()

    # Prepare products grouped by subcategory
    subcategory_products = {}
    for sub in subcategories:
        subcategory_products[sub] = Product.objects.filter(category=sub, is_active=True)

    return render(request, "fashion.html", {
        "fashion_category": fashion_category,
        "subcategory_products": subcategory_products,
    })

from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        sub_category__category=category
    )

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })
from .models import SubCategory, Product

def subcategory_products(request, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    products = Product.objects.filter(sub_category=subcategory)
    return render(request, "subcategory_products.html", {
        "subcategory": subcategory,
        "products": products,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='login')
def wishlist_page(request):
    """
    Renders the wishlist.html template.
    Usually requires querying the database for items belonging to the active user.
    """
    # Fetch all wishlist items for the logged-in user
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    """
    Removes a specific product from the user's wishlist and reloads the page.
    """
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')
