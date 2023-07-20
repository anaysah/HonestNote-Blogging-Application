from django.urls import path
from .views import homeView, blogPage,SearchView, BlogsByCategory

urlpatterns = [
    # path('',views.home, name="home"),
    path('', homeView.as_view(), name='home'),
    path('blog/<slug:slug>', blogPage.as_view(), name='blogPage'),

    path('search/', SearchView.as_view(), name='search_results'),
    path('category/<str:category_name>/', BlogsByCategory.as_view(), name='blogs_by_category'),

    # path('addBlog', addBlog.as_view(), name='addBlog'),
    # path('editBlog/<slug:slug>', editBlog.as_view(), name='editBlog'),
    # path('deleteBlog/<slug:slug>', deleteBlog.as_view(), name='deleteBlog'),
    # path('addCategory', addCategory.as_view(), name='addCategory'),
    # path('likeBlog/<slug:slug>',likeBlog,name='likeBlog'),


    # path('Category/<str:cats>/', allBlogCategory, name='allBlogCategory'),
    
]