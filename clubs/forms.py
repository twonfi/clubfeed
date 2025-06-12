from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from core.models import Club


class EditClubForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = 'edit-club-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save'))


    class Meta:
        model = Club
        fields = (
            'name',
            'description',
            'posters',
        )
