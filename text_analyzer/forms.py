from django import forms

class TextAnalyzerForm(forms.Form):
    user_url = forms.Field(
        required=False,
        widget=forms.URLInput()
    )
    user_essay = forms.Field(
        required=False,
        widget=forms.Textarea(),
    )

