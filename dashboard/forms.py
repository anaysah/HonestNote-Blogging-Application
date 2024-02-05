from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'thumbnail', 'thumbnail_url', 'snippet', 'body', 'slug', 'is_draft']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Your name','class':'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['snippet'].widget.attrs.update({'placeholder': 'Your comment', 'class':'form-control','rows':"5"})
        # self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})