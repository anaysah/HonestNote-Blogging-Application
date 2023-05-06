from django import forms
from .models import Post, Category, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Your name','class':'form-control'})
        self.fields['body'].widget.attrs.update({'placeholder': 'Your comment', 'class':'form-control','rows':"5"})

class addBlogForm(forms.ModelForm):
    AuthorName = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control','disabled':True}))
    class Meta:
        model = Post
        fields = ('title', 'AuthorName','category','image','snippet','body','slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'snippet': forms.TextInput(attrs={'class':'form-control'}),
        }

class editBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','snippet','slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'snippet': forms.TextInput(attrs={'class':'form-control'}),
        }

class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }