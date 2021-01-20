from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import logout

from .forms import UserCreateForm, LoginForm


# アカウント作成
class CreateUser(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('list'))
        return render(request, 'register.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'register.html', {'form': form, })


class Login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect(reverse('list'))
        return render(request, 'login.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form, })


def logout_view(request):
    logout(request)
    return redirect('account:login')
