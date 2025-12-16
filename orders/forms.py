from django import forms
from .models import DesignOrder

class DesignOrderForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ["package", "design_type", "size", "brief"]
        widgets = {
            "brief": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap form-control styling
        for name, field in self.fields.items():
            if name == "package":
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})

            if name == "design_type":
                field.widget.attrs.update({"placeholder": "e.g. logo, poster, branding"})
            if name == "size":
                field.widget.attrs.update({"placeholder": "e.g. A4, 1080x1350, large"})
            if name == "brief":
                field.widget.attrs.update({"placeholder": "Describe what you need, your style, colours, text, deadline, etc."})
     

    def clean_brief(self):
        brief = self.cleaned_data.get("brief", "").strip()
        if len(brief) < 20:
            raise forms.ValidationError("Please provide at least 20 characters describing what you need.")
        return brief
