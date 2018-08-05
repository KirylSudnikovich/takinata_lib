from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm, SignInForm


class SignUp(generic.FormView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('polls:index')

        return render(request, 'signup.html', {'form': form})


class SignIn(generic.FormView):
    template_name = 'signin.html'

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:index')
            else:
                return render(request, 'signin.html', {
                    'form': form,
                    'error_message': "incorrect username/password",
                })
        return render(request, 'signin.html', {'form': form})


class SignOut(generic.DetailView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        logout(request)
        return redirect('polls:index')
