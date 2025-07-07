from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from martor.fields import MartorFormField

from clubs.models import Club, Post, ClubImage


class EditClubForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"] = MartorFormField()

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = "edit-club-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("save", "Save"))

    class Meta:
        model = Club
        fields = (
            "name",
            "description",
            "posters",
        )


class EditPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = "edit-post-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("save", "Save"))

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            "allow_comments",
        )


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = ClubImage
        fields = (
            "image",
            "name",
            "alt",
        )

    def __init__(self, *args, **kwargs):
        access = kwargs.get("access")
        kwargs.pop("access")

        super().__init__(*args, **kwargs)

        if "p" in access:
            self.fields["show_on_club_page"] = forms.BooleanField(
                label="Show on club page", required=False)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = "media-upload-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("upload", "Upload"))


class EditMediaForm(forms.ModelForm):
    class Meta:
        model = ClubImage
        fields = [
            "name",
            "alt",
        ]

    def __init__(self, *args, **kwargs):
        access = kwargs.get("access")
        kwargs.pop("access")
        f = kwargs.get("instance")

        super().__init__(*args, **kwargs)

        if "p" in access:
            self.fields["show_on_club_page"] = forms.BooleanField(
                label="Show on club page", required=False,
                initial=f.show_on_club_page)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = "edit-media-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("save", "Save"))

        if "d" in access:
            self.helper.add_input(
                Submit("delete", "Delete", css_class="btn-danger")
            )
