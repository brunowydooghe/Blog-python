from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Page
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Post, Category
from .forms import ContactForm, PostForm, EditForm
from .forms import UserCreateForm


class PostList(generic.ListView):
    queryset = Post
    template_name = 'blog/index.html'  # a list of all posts will be displayed on index.html

    def get_queryset(self):
        g = Post.objects.filter(status=1).order_by('-created_on')
        return g

    def get_context_data(self, *args, **kwargs):
        context = super(PostList, self).get_context_data(*args, **kwargs)
        context['cat_menu_list'] = Category.objects.all()
        return context


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # detail about each blog post will be on post_detail.html


def contact_form(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = ['info@dominusoft.co']
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponse('Success...Your email has been sent')
    return render(request, 'blog/contact.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
               #first_name=form.cleaned_data['first_name'],
                #last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'blog/signup.html', {'form': form})


# class AddCategoryView(CreateView):
#     model = Category
#     template_name = 'add_category.html'
#     fields = '__all__'


class HomeView(ListView):
    model = Post
    template_name = 'blog/index.html'
    cats = Category.objects.all()

    # ordering = ['-id']
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context['cat_menu_list'] = Category.objects.all()
        print(cat_menu_list)
        return context


def CategoryListView(request, cats):
    cat_menu_list = Category.objects.all()
    return render(request, 'blog/base.html', {'cat_menu_list':cat_menu_list})





class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def index(request):
        # Obtain the context from the HTTP request.
        context = RequestContext(request)

        # Query the database for a list of ALL categories currently stored.
        # Order the categories by no. likes in descending order.
        # Retrieve the top 5 only - or all if less than 5.
        # Place the list in our context_dict dictionary which will be passed to the template engine.
        category_list = Category.objects.order_by('-likes')[:5]
        context_dict = {'categories': category_list}

        # Render the response and send it back!
        return render(request, 'blog/base.html', context_dict, context)
def aboutus(request):
    return render(request, 'blog/aboutus.html')

def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(None, 'blog/categories.html.html', context_dict, context)
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_post.html"


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy('home')

class UserRegisterView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = ExampleModel.objects.get(pk=course_id)
#             m.model_pic = form.cleaned_data['image']
#             m.save()
#             return HttpResponse('image upload success')
#     return HttpResponseForbidden('allowed only via POST')