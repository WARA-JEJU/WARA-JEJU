from django.contrib.auth import login
from django.shortcuts import render, redirect
from . import forms


# Create your views here.
def home(request):
    return render(request, 'index2.html')


def sign_up(request):
    form = forms.SignUpForm

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        print(request)

        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'sign_up.html', {'form': form})
