from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


# get_object_or_404 -> mean get this object or return 404


def home(request):
    context = {
        'posts': Post.objects.all()

    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # now newest post will be at top
    paginate_by = 5  # 2 post per page
    


def LikeView(request, pk):
    # whatever that post_id is look that up in our Post table and 
    # assign it to the post varible or return 404
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    #  save like as well as user to a table called likes
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args= [str(pk)]))


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_like()
        liked = False
        if stuff.likes.filter(id = self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked']=liked
        return context
    

#  when you make change in model, that change does not appear on html page then its problem of view ! can be fixed from here.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'snippet', 'header_image']

    def form_valid(self, form):
        # the form you are trying to submit belongs to current login user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'snippet', 'header_image']

    def form_valid(self, form):
        # the form you are trying to submit belongs to current login user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin,):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
