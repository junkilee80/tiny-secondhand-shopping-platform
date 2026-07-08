from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", "description", "price", "image")

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title and len(title.strip()) < 2:
            raise forms.ValidationError("상품명은 최소 2자 이상이어야 합니다.")

        return title

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price <= 0:
            raise forms.ValidationError("가격은 1원 이상이어야 합니다.")

        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            max_size = 2 * 1024 * 1024

            if image.size > max_size:
                raise forms.ValidationError("이미지 크기는 2MB 이하만 가능합니다.")

            allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
            filename = image.name.lower()

            if not any(filename.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("이미지는 jpg, jpeg, png, gif 파일만 가능합니다.")

        return image