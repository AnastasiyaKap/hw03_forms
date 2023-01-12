from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm
from .utils import get_page


def index(request):
    context = get_page(Post.objects.select_related('group').all(), request)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.select_related('group').all()
    context = {
        'group': group,
        'post_list': post_list
    }
    context.update(get_page(group.posts.all(), request))
    return render(request, 'posts/group_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_list = (Post.objects.select_related('author')
                  .filter(author=post.author))
    context = {
        'post': post,
        'posts_list': posts_list
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
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
    context = {
        'author': author,
    }
    context.update(get_page(author.posts.all(), request))
    return render(request, 'posts/profile.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None)
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
