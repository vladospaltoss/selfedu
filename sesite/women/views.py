from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from .models import *
from .forms import *
from .utils import *
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView

# Create your views here.

class WomenHome(DataMixin ,ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

# def index(request):
#     posts = Women.objects.all()

#     context = {
#         'title' : 'Глвная страница',
#         'posts' : posts,
#         'cat_selected' : 0,
#         }
#     return render(request, 'women/index.html', context)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj':page_obj ,'title':'O сайте'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('404')


class AddPage(LoginRequiredMixin ,DataMixin ,CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    login_url = reverse_lazy('home')
    # raise_exception = True / Генерация страницы 403

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')

#     else:
#         form = AddPostForm()

#     context = {
#         'title' : "Добавление статьи",
#         'form' : form,
#     }

#     return render(request, 'women/addpage.html', context)

# def contact(request):
#     return HttpResponse('Обратная связь')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)

#     context = {
#         'post' : post,
#         # 'menu' : menu,
#         'title' : post.title,
#         'cat_selected' : post.cat_id,
#     }
#     return render(request, 'women/post.html',context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'title' : 'Отображение по рубрикам',
#         'posts' : posts,
#         'cat_selected' : cat_slug,
#         }

#     return render(request, 'women/index.html', context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
        

class LoginUser(DataMixin, LoginView):
    form_class= LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            c_def = self.get_user_context(title='Авторизация')
            return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')