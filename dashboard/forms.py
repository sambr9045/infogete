from django import forms
from . import models


class TicketForm(forms.ModelForm):
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter subject ", "class": "form-control"}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "style": "height:100px!important;",
                "placeholder": "Enter your message",
            }
        )
    )

    class Meta:
        model = models.ticket
        fields = ["subject", "message"]
