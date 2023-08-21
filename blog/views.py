from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.utils.safestring import SafeText
from django.db.models import Q
from .models import Post, Category, FeaturedBlog, JoinUsSubmission
from .forms import  CommentForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django import forms
from django.contrib import messages



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
        

class JoinUsSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder = "Write why you want to join us and how will you help us to grow."
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})

    class Meta:
        model = JoinUsSubmission
        fields = ['name', 'email', 'message']

class JoinusView(CreateView):
    model = JoinUsSubmission
    template_name = 'blog/join_us_form.html'
    form_class = JoinUsSubmissionForm

    def form_valid(self, form):
        response = super().form_valid(form)
        submitted_otp = self.request.POST.get('otp')  # Get submitted OTP
        stored_otp = self.request.session.get('joinus_otp')  # Get stored OTP

        if submitted_otp == stored_otp:
            messages.success(self.request, 'We will review and get back to you soon.')
            return response
        else:
            messages.error(self.request, 'Invalid OTP. Please try again.')
            return response
    
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def generate_otp():
    return ''.join([str(randint(0, 9)) for _ in range(6)])

# Assuming you have access to the request object
def store_otp_in_session(request):
    otp = generate_otp()
    request.session['joinus_otp'] = otp
    request.session.modified = True  # Mark the session as modified
    return otp

def joinus_otp_mail(request):
    email = request.POST.get('email')
    
    try:
        validate_email(email)  # Validate the email using built-in function
    except ValidationError:
        return JsonResponse({'message': 'Invalid email. Please enter a valid email address.'}, status=400)

    otp = store_otp_in_session(request)
    subject = 'Your OTP for Joining Us'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        response = {'message': 'We have sent you an OTP for verification.'}
        return JsonResponse(response)
    except:
        response = {'message': 'There was an error sending the OTP email.'}
        return JsonResponse(response, status=500)
