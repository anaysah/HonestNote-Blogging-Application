from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.utils.safestring import SafeText
from django.db.models import Q
from .models import Post, Category, FeaturedBlog
from .forms import  CommentForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator


class homeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ["-date"]
    paginate_by = 3

    def get_queryset(self):
        # Only show non-drafted posts
        queryset = super().get_queryset()
        return queryset.filter(is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_categories = Category.objects.all()
        context['allCategory'] = all_categories

        # Check if page number is 1 or not present in URL
        page = self.request.GET.get('page')
        if page is None or page == '1':
            featured_blogs = FeaturedBlog.objects.all()
            context['featured_blogs'] = featured_blogs

        return context


class SearchView(homeView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            try:
                # Check if query is a category name
                category = Category.objects.get(name__iexact=query)
                return Post.objects.filter(category=category, is_draft=False)
            except Category.DoesNotExist:
                pass
            
            return Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query), is_draft=False)
        else:
            return super().get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del context['featured_blogs']
        context['category_name'] = self.request.GET.get('query')
        return context

        
class BlogsByCategory(homeView):
    def get_queryset(self):
        category_name = self.kwargs['category_name']
        self.category = Category.objects.get(name__iexact=category_name)
        return Post.objects.filter(category=self.category, is_draft=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del context['featured_blogs']
        context['category_name'] = self.kwargs['category_name']
        return context


class blogPage(FormMixin,DetailView):
    model = Post
    template_name = 'blog/blogPage.html'
    form_class = CommentForm
    def get_success_url(self):
        return reverse('blogPage', kwargs={'slug': self.get_object().slug}) + f"#comment_{self.comment.id}"
    def clean_body_html(self):
        body_html = self.cleaned_data['body']
        return SafeText(body_html)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            self.comment = comment
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 

