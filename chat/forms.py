from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "메시지를 입력하세요. 최대 500자",
                    "class": "form-control",
                }
            )
        }

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()

        if len(content) < 1:
            raise forms.ValidationError("메시지를 입력해야 합니다.")

        if len(content) > 500:
            raise forms.ValidationError("메시지는 최대 500자까지 가능합니다.")

        return content