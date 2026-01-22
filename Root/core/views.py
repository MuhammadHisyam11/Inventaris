from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from .authentication.auth_login import custom_login_required
from .models import Role, User, Product
from .tokens import reset_token_generator

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or "").strip().lower()
        password = request.POST.get('password') or ""

        user = User.objects.filter(email__iexact=email).first()

        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('dashboard')
        
        messages.error(request, 'Invalid email or password.')

        return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')

def logout(request):
    messages.success(request, 'You have been logged out successfully.')
    request.session.flush()
    return redirect('login')

def forget(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()

        user = User.objects.filter(email__iexact=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = reset_token_generator.make_token(user)

            reset_path = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
            reset_link = request.build_absolute_uri(reset_path)

            subject = "Reset password"
            message = (
                f"Klik link ini untuk reset password:\n\n{reset_link}\n\n"
                f"Jika kamu tidak meminta reset, abaikan email ini."
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        
        messages.success(request, 'If an account with that email exists, a recovery email has been sent.')
        messages.error(request, 'email not found.')

        return render(request,"registration/forgot-password.html")

    return render(request, "registration/forgot-password.html")

def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if not user or not reset_token_generator.check_token(user, token):
        return render(request, "registration/reset-invalid.html", status=400)

    if request.method == "POST":
        p1 = request.POST.get("password1") or ""
        p2 = request.POST.get("password2") or ""

        if len(p1) < 8:
            return render(request, "registration/reset-invalid.html", {"error": "Password minimal 8 karakter."})
        if p1 != p2:
            return render(request, "registration/reset-invalid.html", {"error": "Password tidak sama."})

        user.password = make_password(p1)
        user.save(update_fields=["password"])

        return redirect("login")

    return render(request, "registration/reset-invalid.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        
        # Create a new user instance
        user = User(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Registration successful. Please log in.')
        
        return redirect('login')
        
    return render(request, 'registration/register.html')

@custom_login_required
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    product = Product.objects.all()
    count_product = product.count()
    count_user = User.objects.all()
    count_user_admin = count_user.count()
    
    messages.success(request, 'Welcome to the dashboard!')
    
    return render(request, 'dashboard.html', {"user": user, "product": product, "count_product": count_product, "count_user_admin": count_user_admin})

@custom_login_required
def manajement_user(request):
    current_user = User.objects.get(id=request.session['user_id'])

    if current_user.role_id.id != 1:
        return render(request, '404.html')

    users = User.objects.all()
    
    messages.success(request, 'Deleted successfully.')
    
    return render(request,'Page/user_management.html',{'users': users, 'role_id': current_user.role_id, 'user': current_user})

def create(request):
    user = User.objects.get(id=request.session['user_id'])
    
    if user.role_id.id != 1:
        return render(request, '404.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_id = Role.objects.get(id=request.POST.get('role_id'))
        password = make_password(request.POST.get('password'))
        user = User(username=username, email=email, password=password, role_id=role_id)
        user.save()
        
        messages.success(request, 'User created successfully.')
        messages.error(request, 'Failed to create user.')

        return redirect('management-user')

    return render(request, 'Page/create_user.html', {'user': user})

@custom_login_required
def update_user(request, id):
    user = User.objects.get(id=id)
    
    if user.role_id.id not in [2, 3]:
        return render(request, '404.html')

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.role_id = Role.objects.get(id=request.POST.get('role_id'))

        password = request.POST.get('password')
        if password:
            user.password = make_password(password)

        user.save()
        return redirect('management-user')

    return render(request, 'Page/edit_user.html', {'user': user})

@custom_login_required
def delete_user(request, id):
    current_user = User.objects.get(id=request.session['user_id'])

    if current_user.role_id.id != 1:
        return render(request, '404.html')

    if current_user.id == id:
        return render(request, '404.html')

    User.objects.filter(id=id).delete()
    
    messages.success(request, 'Deleted successfully.')
    
    return redirect('management-user')

@custom_login_required
def inventory(request):
    current_user = User.objects.get(id=request.session['user_id'])
    products = Product.objects.all()
    
    if current_user.role_id.id not in [1,2,3]:
        return render(request, '404.html')

    users = User.objects.all()
    return render(request,'Page/inventory.html',{'users': users, 'role_id': current_user.role_id, 'user': current_user, 'products': products})

def create_inv(request):
    user = User.objects.get(id=request.session['user_id'])
    
    if user.role_id.id not in [1, 2]:
        return render(request, '404.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        product = Product(name=name, description=description, price=price, stock=stock)
        product.save()

        return redirect('inventory')

    return render(request, 'Page/create_inventory.html', {'user': user})

def buy(request, id):
    user = User.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, id=id)

    if user.role_id.id not in [1, 2, 3]:
        return render(request, '404.html')

    if product.stock > 0:
        product.stock -= 1
        product.save()
        messages.success(request, 'Purchase successful!')
    else:
        messages.error(request, 'Product is out of stock.')

    return redirect('inventory')

@custom_login_required
def update_inventory(request, id):
    user = User.objects.get(id=request.session['user_id'])
    products = Product.objects.get(id=id)
    
    if user.role_id.id not in [1, 2, 3]:
        return render(request, '404.html')

    if request.method == 'POST':
        products.name = request.POST.get('name')
        products.description = request.POST.get('description')
        products.price = request.POST.get('price')
        products.stock = request.POST.get('stock')

        products.save()
        return redirect('inventory')

    return render(request, 'Page/edit_inventory.html', {'products': products, 'user': user})

@custom_login_required
def delete_inventory(request, id):
    current_user = User.objects.get(id=request.session['user_id'])

    if current_user.role_id.id not in [1, 2]:
        return render(request, '404.html')

    if current_user.id == id:
        return render(request, '404.html')

    Product.objects.filter(id=id).delete()
    return redirect('inventory')