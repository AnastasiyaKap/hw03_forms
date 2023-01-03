from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Group, Post, User
from .forms import PostForm

NUMBERS_POSTS_ON_PAGES = 10
NUMBERS_PAGES = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUMBERS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter()[:NUMBERS_POSTS_ON_PAGES]
    paginator = Paginator(post_list, NUMBERS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Группа {slug}'
    context = {
        'page_obj': page_obj,
        'group': group,
        'title': title
    }
    return render(request, 'posts/group_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_list = (Post.objects.select_related('author')
                  .filter(author=post.author))
    posts_count = posts_list.count()
    context = {
        'post': post,
        'posts_count': posts_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = posts.count()
    paginator = Paginator(posts, NUMBERS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'post_list': posts,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post.id)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {
        'form': form,
        'post': post,
        'is_edit': is_edit})
