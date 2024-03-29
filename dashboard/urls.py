from django.urls import path
from .views import DashboardLoginView, DashboardView, AddBlogView, EditBlogView
from .views_ajax import update_is_Draft, upload_image, delete_image
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', DashboardLoginView.as_view(), name='login'),
    path('', DashboardView.as_view(), name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add/', AddBlogView.as_view(), name='add'),
    path('edit/<int:pk>/', EditBlogView.as_view(), name='edit'),

    path('ajax/update_is_draft/',update_is_Draft,name='update_is_Draft'),
    path('ajax/upload_image/',upload_image,name='upload_image'),
    path('ajax/delete_image',delete_image,name='delete_image')
]