from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from martor.fields import MartorFormField

from .models import Profile


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"] = MartorFormField()

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = "edit-club-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("save", "Save"))

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "picture",
            "description",
        )
