from postbox.models import *
from django.forms import  ModelForm
from django import forms

class CategoryForm(ModelForm):
    category = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'category'}))
    class Meta:
        model=Categories
        fields=['category']


class PostsForm(ModelForm):
    def __init__(self, uname, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        self.fields['cid'] = forms.ModelChoiceField( queryset=Categories.objects.filter(owner=uname),help_text='category')
        self.fields['image']=forms.ImageField(required=False)

    class Meta:
        model = Posts
        fields = ['title','status','cid','image']

class CommentForm(ModelForm):
    comment = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={'placeholder': 'Add your comment'}))
    class Meta:
        model=Comments
        fields=['comment']

