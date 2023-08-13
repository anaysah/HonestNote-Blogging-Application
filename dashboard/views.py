from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView, FormView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import redirect
from django.db import IntegrityError

from django import forms
from blog.models import Post, Image
# from ckeditor.widgets import CKEditorWidget


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboard/dashboard.html"
    login_url = "login"
    model = Post
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date')    
    
class AddBlogView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        slug = slugify(title)
        
        try:
            new_post = Post.objects.create(title=title, slug=slug, author=request.user)
        except IntegrityError:
            existing_post = Post.objects.filter(slug=slug).first()
            if existing_post:
                slug = f"{slug}-{existing_post.id + 1}"
                new_post = Post.objects.create(title=title, slug=slug, author=request.user)

        return redirect('edit', pk=new_post.pk)
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'thumbnail', 'thumbnail_url', 'snippet', 'body', 'is_draft']
        

class EditBlogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView ):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/editBlog.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'


    def test_func(self):
        post = self.get_object()
        # Check if the current user is the author of the post
        #so user cant able to change other post
        return self.request.user == post.author
    
    def form_valid(self, form):
        post = form.instance
        if form.has_changed() and 'title' in form.changed_data:
            existing_post = Post.objects.filter(slug=post.slug).first()
            new_slug = slugify(form.cleaned_data['title'])
            if existing_post:
                new_slug = slugify(f"{form.cleaned_data['title']}_{post.pk+2}")
                
            post.slug = new_slug

        return super().form_valid(form)

class ckeditorView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/ckeditor.html"
