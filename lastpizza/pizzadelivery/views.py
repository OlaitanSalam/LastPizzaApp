from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Pizza, Cart, CartItem, Order,OrderItem
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
import stripe
from django.conf import settings
from django.template.loader import render_to_string
from .forms import CustomUserChangeForm
from django.core.mail import send_mail




stripe.api_key = settings.STRIPE_SECRET_KEY

#your views here

def home(request):
    pizzas = Pizza.objects.all()
    cart = None
    pizza_in_cart = {}

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Create a dictionary to store pizza quantities in the cart
        for item in cart.items.all():
            pizza_in_cart[item.pizza.id] = item.quantity
    else:
        pizza_in_cart = {}  # No cart if the user is not authenticated

    return render(request, 'pizzadelivery/home.html', {'pizzas': pizzas, 'cart': cart, 'pizza_in_cart': pizza_in_cart})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to the homepage or another page after registration
    else:
        form = CustomUserCreationForm()  # Display the empty form for GET request
    return render(request, "pizzadelivery/register.html", {"form": form})


def login_view(request):
    form = CustomLoginForm()  # Create an instance of your login form
    if request.method == "POST":
        form = CustomLoginForm(request.POST)  # Bind form with POST data
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in
                return redirect("home")  # Redirect to the home page after successful login
            else:
                messages.error(request, "We could not locate a Pizza Profile with that e-mail and password combination. Please make sure you are using the e-mail address associated with your Pizza Garden's Profile")  # Display error message
    return render(request, "pizzadelivery/login.html", {"form": form})  # Pass form to the template

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect("home")  # Redirect to the homepage after logout




@login_required
def add_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)

    if not item_created:
        cart_item.quantity += 1
    cart_item.save()

    cart_items_html = render_to_string('pizzadelivery/cart_items.html', {'cart': cart})
    response_data = {
        'total_items': cart.items.count(),
        'total_price': cart.total_price(),
        'cart_items_html': cart_items_html,
    }
    return JsonResponse(response_data)

@login_required
def remove_from_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    cart = Cart.objects.get(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, pizza=pizza).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    cart_items_html = render_to_string('pizzadelivery/cart_items.html', {'cart': cart})
    response_data = {
        'total_items': cart.items.count(),
        'total_price': cart.total_price(),
        'cart_items_html': cart_items_html,
    }
    return JsonResponse(response_data)





@login_required
def delete_from_cart(request, pizza_id):
    cart = Cart.objects.get(user=request.user)
    pizza = get_object_or_404(Pizza, id=pizza_id)
    cart_item = CartItem.objects.filter(cart=cart, pizza=pizza).first()

    if cart_item:
        cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
        cart_items_html = render_to_string('pizzadelivery/cart_items.html', {'cart': cart})
        return JsonResponse({
            'total_items': cart.items.count(),
            'total_price': cart.total_price(),
            'cart_items_html': cart_items_html,
        })

    return redirect('home')



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the updated user data (including address)
            return redirect('billing')  # Redirect to the billing page
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'pizzadelivery/checkout.html', {'cart': cart, 'form': form})



@login_required
def billing(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Ensure the cart is not empty
    if cart.items.count() == 0:
        return redirect('home')

    # Calculate total price
    total_price = cart.total_price()

    # Create Stripe Payment Intent and Order if they don't exist
    try:
        # Create PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Convert to cents
            currency="usd",
            metadata={"user_id": request.user.id},
        )

        # Create an Order for the user
        order, created = Order.objects.get_or_create(
            user=request.user,
            total_price=total_price,
            stripe_payment_intent_id=intent["id"],
            country=request.user.country,
            billing_address=request.user.address,
        )

       

        # Render the billing page with client_secret and order_id
        return render(request, "pizzadelivery/billing.html", {
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "cart": cart,
            "client_secret": intent["client_secret"],
            "order_id": order.id,
        })

    except stripe.error.StripeError as e:
        print("Stripe Error:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

    return redirect('home')



@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_paid = True
    order.save()

    cart = Cart.objects.get(user=request.user)
    
    # Move Cart Items to Order Items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            pizza=cart_item.pizza,
            quantity=cart_item.quantity,
            price=cart_item.pizza.price  # Save price at the time of order
        )

    # Clear cart after order is completed
    cart.delete()

    # Send confirmation email
    send_mail(
        subject="Order Confirmation",
        message=f"Your order {order.id} has been placed successfully!",
        from_email="olaitan2hola@gmail.com",
        recipient_list=[request.user.email],
    )

    return render(request, 'pizzadelivery/order_success.html', {"order": order})


@login_required
def order_failed(request):
    return render(request, "pizzadelivery/order_failure.html")

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_paid=True).order_by("-created_at")  # Fetch user orders

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, "pizzadelivery/profile.html", {"form": form, "orders": orders})
