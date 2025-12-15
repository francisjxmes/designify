from django import forms
from .models import Deliverable

class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ["file", "note"]
