from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("reason",)
        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "신고 사유를 입력하세요. 최대 500자",
                    "class": "form-control",
                }
            )
        }

    def clean_reason(self):
        reason = self.cleaned_data.get("reason", "").strip()

        if len(reason) < 5:
            raise forms.ValidationError("신고 사유는 최소 5자 이상 입력해야 합니다.")

        if len(reason) > 500:
            raise forms.ValidationError("신고 사유는 최대 500자까지 가능합니다.")

        return reason