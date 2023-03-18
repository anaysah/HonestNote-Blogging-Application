from django.urls import path
from .views import UserCreation

urlpatterns = [
    path('signup/',UserCreation.as_view(), name="signup")
]