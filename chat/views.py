from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from products.models import Product

from .forms import MessageForm
from .models import Message


@login_required
def global_chat(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.is_suspended:
        return HttpResponseForbidden("휴면 계정은 채팅을 사용할 수 없습니다.")

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.is_global = True
            message.save()
            return redirect("chat:global")
    else:
        form = MessageForm()

    messages = (
        Message.objects
        .filter(is_global=True)
        .select_related("sender")
        .order_by("created_at")
    )

    return render(
        request,
        "chat/global_chat.html",
        {
            "form": form,
            "messages": messages,
        },
    )


@login_required
def inbox(request):
    messages = (
        Message.objects
        .filter(is_global=False)
        .filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related("sender", "receiver", "product")
        .order_by("-created_at")
    )

    conversations = []
    seen = set()

    for message in messages:
        if not message.product or not message.receiver:
            continue

        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender

        key = (message.product.id, other_user.id)

        if key in seen:
            continue

        seen.add(key)

        conversations.append({
            "product": message.product,
            "other_user": other_user,
            "last_message": message,
        })

    return render(
        request,
        "chat/inbox.html",
        {
            "conversations": conversations,
        },
    )


@login_required
def direct_chat(request, product_id, user_id):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.is_suspended:
        return HttpResponseForbidden("휴면 계정은 메시지를 보낼 수 없습니다.")

    product = get_object_or_404(Product, id=product_id, is_blocked=False)
    other_user = get_object_or_404(User, id=user_id)

    if request.user == other_user:
        return HttpResponseForbidden("자기 자신과는 대화할 수 없습니다.")

    # 구매자는 해당 상품의 판매자와만 대화할 수 있다.
    # 판매자는 문의한 사용자에게 답장할 수 있다.
    if request.user != product.seller and other_user != product.seller:
        return HttpResponseForbidden("해당 상품 판매자와만 대화할 수 있습니다.")

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.product = product
            message.is_global = False
            message.save()
            return redirect(
                "chat:direct",
                product_id=product.id,
                user_id=other_user.id,
            )
    else:
        form = MessageForm()

    messages = (
        Message.objects
        .filter(is_global=False, product=product)
        .filter(
            Q(sender=request.user, receiver=other_user)
            | Q(sender=other_user, receiver=request.user)
        )
        .select_related("sender", "receiver", "product")
        .order_by("created_at")
    )

    return render(
        request,
        "chat/direct_chat.html",
        {
            "form": form,
            "messages": messages,
            "product": product,
            "other_user": other_user,
        },
    )