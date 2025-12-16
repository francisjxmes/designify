from django import forms
from .models import Deliverable


class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ["file", "note"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["note"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Optional note for the client"
            }
        )
