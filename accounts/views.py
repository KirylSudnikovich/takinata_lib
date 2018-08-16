from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm, SignInForm
from lib.controllers.user import UserController


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
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
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
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tracker:home')
            else:
                return render(request, 'accounts/signin.html', {
                    'form': form,
                    'error_message': "incorrect username/password",
                })
        return render(request, 'accounts/signin.html', {'form': form})


class SignOut(generic.DetailView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        logout(request)
        return redirect('tracker:home')
