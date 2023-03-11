from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Post, Group, User, Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView,
                                  CreateView, DeleteView,
                                  UpdateView, View)
from django.utils.decorators import method_decorator
from .forms import PostForm, CommentForm
from .utils import DataMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy


class PostsHome(DataMixin, ListView):
    model = Post
    template_name = 'posts/index.html'

    def get_queryset(self):
        return Post.objects.all()


class GroupPosts(DataMixin, ListView):
    model = Post
    template_name = 'posts/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(group=get_object_or_404(Group,
                                      slug=self.kwargs['group_slug']))
        context.update(c_def)
        return context

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['group_slug'])
        return group.posts.select_related('group')


class Profile(DataMixin, ListView):
    model = Post
    template_name = 'posts/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.posts.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        c_def = self.get_user_context(author=author,
                                      following=False)
        if self.request.user.is_authenticated:
            c_def['following'] = Follow.objects.filter(
                user=self.request.user, author=author
            )
        context.update(c_def)
        return context


class PostDetail(DataMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        c_def = self.get_user_context(requser=self.request.user,
                                      comments=post.comments.select_related(
                                          'post'),
                                      form=CommentForm(
                                          self.request.POST or None))
        context.update(c_def)
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_post.html'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user})

    def form_valid(self, form):
        author = Post(author=self.request.user)
        form = PostForm(
            self.request.POST,
            files=self.request.FILES,
            instance=author
        )
        form.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/delete_post.html'
    model = Post
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('posts:profile',
                            kwargs={'username': self.request.user})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.author:
            success_url = self.get_success_url()
            self.object.delete()
            return redirect(success_url)
        return redirect('posts:index')


class PostEditView(DataMixin, UpdateView):
    template_name = 'posts/create_post.html'
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('posts:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(edit=True)
        context.update(c_def)
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('posts:post_detail', post_id=kwargs['post_id'])
        return super(PostEditView, self).dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_detail.html'
    form_class = CommentForm

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse(
            'posts:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.get_object()
        comment.save()
        return super().form_valid(form)


class FollowView(LoginRequiredMixin, DataMixin, ListView):
    model = Post
    template_name = 'posts/follow.html'

    def get_queryset(self):
        return Post.objects.filter(
            author__following__user=self.request.user
        )


class AddFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        author = get_object_or_404(User, username=self.kwargs['username'])
        if user == author:
            return redirect('posts:profile', username=kwargs['username'])
        Follow.objects.get_or_create(user=user, author=author)

        return redirect('posts:profile', username=kwargs['username'])


class UnfollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        follow = get_object_or_404(
            Follow, user=request.user, author__username=self.kwargs['username']
        )
        if follow:
            follow.delete()
        return redirect('posts:profile', username=self.kwargs['username'])
