from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.models import Profile

from .forms import TransferForm
from .models import Transfer


@login_required
def transfer_points(request):
    sender_profile, _ = Profile.objects.get_or_create(user=request.user)

    if sender_profile.is_suspended:
        return HttpResponseForbidden("휴면 계정은 송금할 수 없습니다.")

    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            receiver_username = form.cleaned_data["receiver_username"]
            amount = form.cleaned_data["amount"]
            memo = form.cleaned_data["memo"]

            try:
                receiver = User.objects.get(username=receiver_username)
            except User.DoesNotExist:
                form.add_error("receiver_username", "존재하지 않는 사용자입니다.")
                return render(request, "payments/transfer_form.html", {"form": form})

            if receiver == request.user:
                form.add_error("receiver_username", "자기 자신에게는 송금할 수 없습니다.")
                return render(request, "payments/transfer_form.html", {"form": form})

            receiver_profile, _ = Profile.objects.get_or_create(user=receiver)

            if receiver_profile.is_suspended:
                form.add_error("receiver_username", "휴면 계정에게는 송금할 수 없습니다.")
                return render(request, "payments/transfer_form.html", {"form": form})

            with transaction.atomic():
                sender_profile = Profile.objects.select_for_update().get(user=request.user)
                receiver_profile = Profile.objects.select_for_update().get(user=receiver)

                if sender_profile.points < amount:
                    form.add_error("amount", "보유 포인트보다 큰 금액은 송금할 수 없습니다.")
                    return render(request, "payments/transfer_form.html", {"form": form})

                sender_profile.points -= amount
                receiver_profile.points += amount

                sender_profile.save()
                receiver_profile.save()

                Transfer.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    amount=amount,
                    memo=memo,
                )

            return redirect("payments:history")
    else:
        form = TransferForm()

    return render(request, "payments/transfer_form.html", {"form": form})


@login_required
def transfer_history(request):
    transfers = (
        Transfer.objects
        .filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related("sender", "receiver")
        .order_by("-created_at")
    )

    return render(
        request,
        "payments/transfer_history.html",
        {
            "transfers": transfers,
        },
    )
