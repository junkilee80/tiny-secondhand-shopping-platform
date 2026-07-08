from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.models import Profile

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