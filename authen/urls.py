from django.urls import path
from .views import UserCreation, UserEdit

urlpatterns = [
    path('signup/',UserCreation.as_view(), name="signup"),
    path('UserEdit/',UserEdit.as_view(), name="UserEdit"),
]