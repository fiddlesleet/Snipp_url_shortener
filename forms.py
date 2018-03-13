from django import forms
from .validators import validate_url, validate_dot_com


class SubmitUrlForms(forms.Form):
    url = forms.CharField(
        label='',
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Long URL",
                "class": "form-control"
            }
        )
    )

    #
    # def clean(self):
    #     cleaned_data = super(SubmitUrlForms, self).clean()
    #     url = cleaned_data.get('url')
    #

    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError("Invalid url entered")
    #     return url