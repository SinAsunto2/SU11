from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileEditForm

from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user.is_online = True  # Marcar como en línea
                user.save()

                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        login_form = LoginForm()

    return render(request, 'registration/login.html', {'login_form': login_form})


def logout_view(request):
    if request.user.is_authenticated:
        # Cambiar el estado a "Offline" antes de cerrar la sesión
        request.user.is_online = False
        request.user.save()
        
        logout(request)
    return redirect('index')  # Redirige a la página de inicio


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu foto de perfil se actualizó correctamente.')
            return redirect('edit_profile')  # Reemplaza 'profile' con el nombre de tu vista de perfil.
        else:
            messages.error(request, 'Hubo un error al actualizar tu foto de perfil. Por favor, inténtalo de nuevo.')
    else:
        form = ProfileEditForm(instance=request.user)

    context = {
        'active_page': 'profile',
        'form': form
    }

    return render(request, 'account/profile.html', context)