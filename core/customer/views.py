from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BasicUserForm, BasicCustomerForm

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required()
def home(request):
    print(request)
    return redirect(reverse('customer:profile'))


@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = BasicUserForm(instance=request.user)
    customer_form = BasicCustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)

    if request.POST.get('action') == 'update_profile':
        user_form = BasicUserForm(
            request.POST, instance=request.user)
        customer_form = BasicCustomerForm(
            request.POST, request.FILES, instance=request.user.customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()

            messages.success(request, 'Your profile has been updated')
            return redirect(reverse('customer:profile'))

    elif request.POST.get('action') == 'update_password':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Your password has been updated')
            return redirect(reverse('customer:profile'))

    return render(request, 'customer/profile.html', {
        "user_form": user_form,
        "customer_form": customer_form,
        "password_form": password_form
    })
