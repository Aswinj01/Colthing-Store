from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from accounts.models import Account


def user_login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")

            # 🔥 THIS IS IMPORTANT
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('home')

        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name') or ""
        last_name = request.POST.get('last_name') or ""
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'accounts/register.html')

@require_POST
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')