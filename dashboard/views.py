from django.contrib.auth.views import LoginView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url = "login"
