from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.http import JsonResponse


def Signup_api(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            print(user)
            
            login(request, user)
            messages.success(request, 'Signup successful. Welcome!')
            return redirect('dashboard')  
        else:
            
            messages.error(request, 'Error during signup. Please try again.')  # Show an error message if form is invalid
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def Login_api(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('Login successful')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard_api(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def profile_api(request):
    return render(request, 'accounts/profile.html')


def forgot_password_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({"error": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No user found with this email."}, status=404)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{request.scheme}://{request.get_host()}/accounts/reset-password/{uid}/{token}/"

        # Email template rendering
        subject = "Password Reset Request"
        email_template_name = "accounts/password_reset_email.txt"
        context = {
            "user": user,
            "reset_url": reset_url,
        }
        email_content = render_to_string(email_template_name, context)

        try:
            email_message = EmailMessage(subject, email_content, to=[email])
            email_message.send()
        except Exception as e:
            return JsonResponse({"error": "Failed to send email.", "details": str(e)}, status=500)

        return JsonResponse({"message": "Password reset email sent successfully."}, status=200)

    return render(request, 'accounts/forgot_password.html')