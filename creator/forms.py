from django import forms

from core.models import Post, Club


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.get('queryset')
        kwargs.pop('queryset')
        super().__init__(*args, **kwargs)

        self.fields['club'].queryset = queryset


    class Meta:
        model = Post
        fields = (
            'club',
            'title',
            'body',
        )
