from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm, SignInForm
from lib.controllers.user import UserController
from lib.storage.user import UserStorage


class SignUp(generic.FormView):
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        response = redirect('tracker:home')
        error1 = ''
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            users = UserStorage.get_all_users()
            have = False
            for u in users:
                if email == u.email:
                    have = True
                    error1 = "An account with this name is already registered"
            if not have:
                user = form.save()
                user.refresh_from_db()
                user.save()
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                UserController.reg(user.username, user.password, email)
                response.set_cookie(key='have_account', value='1')
                return response
        return render(request, 'accounts/signup.html', {'form': form, 'error1': error1})


class SignIn(generic.FormView):
    template_name = 'accounts/signin.html'

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'accounts/signin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserStorage.get_user_by_name(username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('tracker:home')
                response.set_cookie(key='have_account', value='1')
                return response
            else:
                if user is None:
                    error = "Incorrect username"
                elif user.password != password:
                    error = "Incorrect password"
                return render(request, 'accounts/signin.html', {
                    'form': form,
                    'error_message': error,
                })
        return render(request, 'accounts/signin.html', {'form': form})


class SignOut(generic.DetailView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        logout(request)
        return redirect('tracker:home')
