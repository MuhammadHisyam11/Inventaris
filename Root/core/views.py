from datetime import timezone
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from .models import User
from .tokens import reset_token_generator

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def base(request):
    return render(request, 'base.html')

def dashboard(request):
    return render(request, 'dashboard.html')

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