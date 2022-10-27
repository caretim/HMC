

from django import forms
from .models import Comment

class MakeCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


