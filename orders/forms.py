from django import forms
from .models import DesignOrder

class DesignOrderForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ["package", "design_type", "size", "brief"]
        widgets = {
            "brief": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_brief(self):
        brief = self.cleaned_data.get("brief", "").strip()
        if len(brief) < 20:
            raise forms.ValidationError("Please provide at least 20 characters describing what you need.")
        return brief
