from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.utils.safestring import SafeText
from django.db.models import Q
from .models import Post, Category
from .forms import addBlogForm, editBlogForm, addCategoryForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

def search_results(request):
    query = request.GET.get('query')
    object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    return render(request, 'home.html', {'object_list': object_list})

class homeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ["-date"]
    def get_context_data(self,*args, **kwargs):
        allCategory = Category.objects.all()
        context = super(homeView,self).get_context_data(*args,**kwargs)
        context['allCategory'] = allCategory
        return context

class blogPage(DetailView):
    model = Post
    template_name = 'blogPage.html'
    def clean_body_html(self):
        body_html = self.cleaned_data['body']
        return SafeText(body_html)
    def get_context_data(self,*args, **kwargs):
        blog = get_object_or_404(Post, slug=self.kwargs['slug'])
        totalLikes = blog.total_likes()
        allCategory = Category.objects.all()
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = super(blogPage,self).get_context_data(*args,**kwargs)
        context['allCategory'] = allCategory
        context['totalLikes'] = totalLikes
        context['liked'] = liked
        return context

def likeBlog(req,slug):
    blog = get_object_or_404(Post, slug=slug)
    user_id = req.user.id
    if blog.likes.filter(id=user_id).exists():
        blog.likes.remove(req.user)
    else:
        blog.likes.add(req.user)
    return HttpResponseRedirect(reverse('blogPage',args=[slug]))


class addBlog(LoginRequiredMixin, CreateView):
    model = Post
    form_class = addBlogForm
    template_name = 'addBlog.html'
    login_url = 'home'
    # fields = '__all__'
    # fields = ('title','body')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user
        initial['AuthorName'] = self.request.user.username
        return initial

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

def allBlogCategory(req, cats):
    try:
        category = Category.objects.get(name__iexact=cats.replace('-',' '))  # Get the Category object
        blogs = Post.objects.filter(category=category)  # Filter the Blog objects by the Category object
    except:
        blogs = None
    return render(req,'allBlogCategory.html' ,{"cats":cats.replace('-',' '),"blogs":blogs} )
