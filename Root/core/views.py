from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from .authentication.auth_login import custom_login_required
from .models import User, Product
from .tokens import reset_token_generator

Role = [1, 2]  # Define valid roles here

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

        return render(request, 'registration/login.html', {'error': 'Invalid email or password.'})

    return render(request, 'registration/login.html')

def logout(request):
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
                fail_silently=False,  # biar kelihatan error kalau SMTP bermasalah
            )

        # selalu tampilkan pesan sama (anti user enumeration)
        return render(
            request,
            "registration/forgot-password.html",
            {"message": "If an account with that email exists, a recovery email has been sent."}
        )

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

        return render(request, "registration/login.html")

    return render(request, "registration/reset-invalid.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        
        # Create a new user instance
        user = User(username=username, email=email, password=password)
        user.save()
        
        return render(request, 'registration/login.html', {'message': 'Registration successful. Please log in.'})
        
    return render(request, 'registration/register.html')

@custom_login_required
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    product = Product.objects.all()
    count_product = product.count()
    count_user = User.objects.all()
    count_user_admin = count_user.count()
    return render(request, 'dashboard.html', {"user": user, "product": product, "count_product": count_product, "count_user_admin": count_user_admin})

@custom_login_required
def manajement_user(request):
    current_user = User.objects.get(id=request.session['user_id'])

    if current_user.role_id not in [1]:
        return render(request, '404.html')

    users = User.objects.all()
    return render(request,'Page/user_management.html',{'users': users, 'role_id': current_user.role_id, 'user': current_user})

@custom_login_required
def inventory(request):
    current_user = User.objects.get(id=request.session['user_id'])

    if current_user.role_id not in Role:
        return render(request, '404.html')

    users = User.objects.all()
    return render(request,'Page/inventory.html',{'users': users, 'role_id': current_user.role_id, 'user': current_user})