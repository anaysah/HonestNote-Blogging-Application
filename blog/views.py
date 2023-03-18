from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.utils.safestring import SafeText
from .models import Post, Category
from .forms import addBlogForm, editBlogForm, addCategoryForm
from django.urls import reverse_lazy


class homeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ["-date"]

class blogPage(DetailView):
    model = Post
    template_name = 'blogPage.html'
    def clean_body_html(self):
        body_html = self.cleaned_data['body']
        return SafeText(body_html)
    
class addBlog(CreateView):
    model = Post
    form_class = addBlogForm
    template_name = 'addBlog.html'
    # fields = '__all__'
    # fields = ('title','body')

class editBlog(UpdateView):
    model = Post
    form_class = editBlogForm
    template_name = 'editBlog.html'

class deleteBlog(DeleteView):
    model = Post
    template_name = 'deleteBlog.html'
    success_url = reverse_lazy('home')

class addCategory(CreateView):
    model = Category
    form_class = addCategoryForm
    template_name = 'addCategory.html'