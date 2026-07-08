from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from chat.models import Message
from payments.models import Transfer
from products.models import Product
from reports.models import Report
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignUpForm
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, "accounts/profile.html", {"form": form})
@staff_member_required
def admin_dashboard(request):
    context = {
        "user_count": User.objects.count(),
        "product_count": Product.objects.count(),
        "blocked_product_count": Product.objects.filter(is_blocked=True).count(),
        "report_count": Report.objects.count(),
        "suspended_user_count": Profile.objects.filter(is_suspended=True).count(),
        "message_count": Message.objects.count(),
        "transfer_count": Transfer.objects.count(),
    }

    return render(request, "accounts/admin_dashboard.html", context)