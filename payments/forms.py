from django import forms


class TransferForm(forms.Form):
    receiver_username = forms.CharField(
        max_length=150,
        label="받는 사람 아이디",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "받는 사람의 username을 입력하세요",
            }
        ),
    )

    amount = forms.IntegerField(
        min_value=1,
        max_value=1000000,
        label="송금 포인트",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "송금할 포인트",
            }
        ),
    )

    memo = forms.CharField(
        max_length=200,
        required=False,
        label="메모",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "메모를 입력하세요",
            }
        ),
    )

    def clean_receiver_username(self):
        receiver_username = self.cleaned_data.get("receiver_username", "").strip()

        if not receiver_username:
            raise forms.ValidationError("받는 사람 아이디를 입력해야 합니다.")

        return receiver_username

    def clean_memo(self):
        memo = self.cleaned_data.get("memo", "").strip()
        return memo