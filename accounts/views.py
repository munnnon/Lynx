from datetime import date, timedelta

from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import RegisterForm
from accounts.models import Streak
from lessons.models import UserLesson

User = get_user_model()

def update_streak(user):
    """
    Updates the user's learning streak based on completed lessons.

    - If the user completed a lesson today and yesterday, increment streak.
    - If the user did not complete a lesson today and missed yesterday, reset streak to 0.
    - If the user completed a lesson today but not yesterday, start a new streak at 1.
    - Does nothing if no lessons were completed today, but streak was active yesterday.

    Args:
        user (User): The user whose streak should be updated.
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    completed_lessons_today = UserLesson.objects.filter(user = user, completed_at= today).exists()
    streak, _ = Streak.objects.get_or_create(
        user = user,
        defaults={'days_count': 0}
    )
    if streak.last_activity_date is None and not completed_lessons_today:
        return

    if not completed_lessons_today and streak.last_activity_date != yesterday:
        streak.days_count = 0
    elif not completed_lessons_today and streak.last_activity_date == yesterday:
        return
    elif completed_lessons_today and streak.last_activity_date == yesterday:
        streak.days_count += 1
    else:
        streak.days_count = 1
    streak.save()
    return

def register_view(request):
    """
    Handles user registration.

    - Displays a registration form on GET requests.
    - Processes registration on POST requests.
    - Displays form errors using the Django messages framework.

    Args:
       request (HttpRequest): The incoming HTTP request.

    Returns:
       HttpResponse: Renders registration page with form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Konto zostało utworzone! Zaloguj się.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    Handles user login.

    - Authenticates the user using username and password.
    - Redirects to '/lynx' on successful login.
    - Shows an error message if authentication fails.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders login page or redirects after successful login.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/lynx')
        else:
            messages.error(request, 'Nieprawidłowa nazwa lub hasło.')
            return  redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

@login_required(login_url='login')
def account_settings_view (request):
    """
    Displays the account settings page for the logged-in user.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders account settings template with user context.
    """
    user = request.user
    return render(request, 'accounts/account_settings.html', {'user': user})

def change_password_view(request):
    """
    Handles password changes for logged-in users.

    - Processes POST requests to update the password.
    - Uses PasswordChangeForm to validate and save new password.
    - Updates session to prevent logout after password change.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders a password change form or redirects on success.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account_settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })

@csrf_exempt
@login_required(login_url='login')
def change_email(request):
    """
    Allows logged-in users to change their email address.

    - Validates that the new email is not empty and not already taken.
    - Updates user's email and shows a success message.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Redirects to account settings page.
    """
    if request.method == 'POST':

        user = request.user
        email = request.POST.get('email-change')
        if not email:
            messages.error(request, 'Wprowadź email')
            return redirect('account_settings')
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, 'Ten email jest już wykorzystany. Spróbuj inny...')
            return redirect('account_settings')
        user.email = email
        user.save()
        messages.success(request, 'Email użytkownika został zmieniony.')
        return redirect('account_settings')

    return redirect('account_settings')

@csrf_exempt
@login_required(login_url='login')
def change_username(request):
    """
    Allows logged-in users to change their username.

    - Validates that the new username is not empty and not already taken.
    - Updates user's username and shows a success message.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Redirects to account settings page.
    """

    if request.method == 'POST':

        user = request.user
        username = request.POST.get('username-change')
        if not username:
            messages.error(request, 'Wprowadź username')
            return redirect('account_settings')
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'Ten username jest już zajęty. Spróbuj inny...')
            return redirect('account_settings')
        user.username = username
        user.save()
        messages.success(request, 'Nazwa użytkownika została zmieniona.')
        return redirect('account_settings')

    return redirect('account_settings')
