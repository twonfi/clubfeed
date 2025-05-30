from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from core.models import Post


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Only show clubs which the user has post access to
        queryset = kwargs.get('queryset')
        kwargs.pop('queryset')

        super().__init__(*args, **kwargs)

        self.fields['club'].queryset = queryset  # Set club choices

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_id = 'create-post-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('post', 'Post'))


    class Meta:
        model = Post
        fields = (
            'club',
            'title',
            'body',
        )
