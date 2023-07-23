from django.urls import path
from .views import DashboardLoginView, DashboardView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', DashboardLoginView.as_view(), name='login'),
    path('', DashboardView.as_view(), name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]