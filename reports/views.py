from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from products.models import Product

from .forms import ReportForm
from .models import Report


PRODUCT_REPORT_LIMIT = 3
USER_REPORT_LIMIT = 5


@login_required
def report_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_blocked=False)

    if product.seller == request.user:
        return HttpResponseForbidden("본인이 등록한 상품은 신고할 수 없습니다.")

    already_reported = Report.objects.filter(
        reporter=request.user,
        target_type="product",
        target_product=product,
    ).exists()

    if already_reported:
        return HttpResponseForbidden("이미 신고한 상품입니다.")

    if request.method == "POST":
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.target_type = "product"
            report.target_product = product
            report.save()

            report_count = Report.objects.filter(
                target_type="product",
                target_product=product,
            ).count()

            if report_count >= PRODUCT_REPORT_LIMIT:
                product.is_blocked = True
                product.save()

            return redirect("products:list")
    else:
        form = ReportForm()

    return render(
        request,
        "reports/report_form.html",
        {
            "form": form,
            "target_name": product.title,
            "target_type": "상품",
        },
    )


@login_required
def report_user(request, user_id):
    target_profile = get_object_or_404(Profile, user_id=user_id)
    target_user = target_profile.user

    if target_user == request.user:
        return HttpResponseForbidden("자기 자신은 신고할 수 없습니다.")

    already_reported = Report.objects.filter(
        reporter=request.user,
        target_type="user",
        target_user=target_user,
    ).exists()

    if already_reported:
        return HttpResponseForbidden("이미 신고한 사용자입니다.")

    if request.method == "POST":
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.target_type = "user"
            report.target_user = target_user
            report.save()

            report_count = Report.objects.filter(
                target_type="user",
                target_user=target_user,
            ).count()

            if report_count >= USER_REPORT_LIMIT:
                target_profile.is_suspended = True
                target_profile.save()

            return redirect("products:list")
    else:
        form = ReportForm()

    return render(
        request,
        "reports/report_form.html",
        {
            "form": form,
            "target_name": target_user.username,
            "target_type": "사용자",
        },
    )