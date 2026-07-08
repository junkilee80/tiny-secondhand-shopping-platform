from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.filter(is_blocked=False).order_by("-created_at")
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_blocked=False)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def product_create(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.is_suspended:
        return HttpResponseForbidden("휴면 계정은 상품을 등록할 수 없습니다.")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("products:detail", product_id=product.id)
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {"form": form, "title": "상품 등록"})


@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_blocked=False)

    if product.seller != request.user:
        return HttpResponseForbidden("본인이 등록한 상품만 수정할 수 있습니다.")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("products:detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {"form": form, "title": "상품 수정"})


@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_blocked=False)

    if product.seller != request.user:
        return HttpResponseForbidden("본인이 등록한 상품만 삭제할 수 있습니다.")

    if request.method == "POST":
        product.delete()
        return redirect("products:list")

    return render(request, "products/product_confirm_delete.html", {"product": product})