import blog
from django.urls import path

from .models import Category
from .views import HomeView, ArticleDetailView, UpdatePostView, DeletePostView

urlpatterns = [
    path('', blog.views.PostList.as_view(), name='home'),
    #path('', HomeView.as_view(), name="home"),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/remove/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='artivle-detail'),
    path('<slug:slug>', blog.views.PostDetail.as_view(), name='post_detail'),
    path('contact/', blog.views.contact_form, name='contact'),
    path('signup/', blog.views.signup, name='signup'),
    path('category/<str:choices>/', Category, name='category'),
    path('aboutus/',blog.views.aboutus, name='aboutus'),
    ]
