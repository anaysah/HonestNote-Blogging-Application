from django import forms
from .models import Post, Category

class addBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','author','category','body','slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
        }

class editBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
        }

class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }