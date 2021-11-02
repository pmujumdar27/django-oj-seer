from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from seer.models import Problem

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('seer-home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Account Info Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    u_problems = Problem.objects.filter(author=request.user)

    context = {
        'u_form': u_form,
        'u_problems': u_problems,
    }

    return render(request, 'users/profile.html', context)