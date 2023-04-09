from django.forms import ModelForm
from . import models
class CommentForm(ModelForm):
    class Meta:
        model = models.Articles
        fields = "__all__"
