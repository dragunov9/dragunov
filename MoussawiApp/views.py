from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Like, Comment, Notification
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    NotificationSerializer
)
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from .models import Notification
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from rest_framework import generics, permissions
from .models import Comment
from rest_framework import status
from .serializers import CommentSerializer
from django.db.models import Count

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'MoussawiApp/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'MoussawiApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.annotate(comment_count=Count('comments')).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_likes'] = set(user_likes)
        else:
            context['user_likes'] = set()
        return context
       


class UserPostListView(ListView):
    model = Post
    template_name = 'MoussawiApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        comment_counts = {
            post.id: post.comments.count() for post in posts
        }
        context['comment_counts'] = comment_counts

        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_likes'] = set(user_likes)
        else:
            context['user_likes'] = set()
        return context


class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('created_at')
        context['comment_count'] = self.object.comments.count()

        if self.request.user.is_authenticated:
            liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_likes'] = set(liked_posts)
        else:
            context['user_likes'] = set()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'MoussawiApp/newpostform.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'MoussawiApp/newpostform.html'  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'MoussawiApp/about.html', {'title': 'About'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Like, Comment, Notification ViewSets with toggle-like logic:

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')

        if not post_id:
            return Response({"detail": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        like = Like.objects.filter(user=user, post_id=post_id).first()

        if like:
            like.delete()  
            Notification.objects.filter(
                sender=user,
                recipient=like.post.author,
                post_id=post_id,
                type='like'
            ).delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Like (create)
            serializer = self.get_serializer(data={'user': user.id, 'post': post_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Create notification if liker is not the post author
            post = serializer.instance.post
            if post.author != user:
                Notification.objects.create(
                    sender=user,
                    recipient=post.author,
                    post=post,
                    type='like'
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         return self.queryset.filter(recipient=self.request.user, is_read=False).order_by('-timestamp')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        post = comment.post
        user = self.request.user
        if post.author != user:
            Notification.objects.create(
                sender=user,
                recipient=post.author,
                post=post,
                type='comment'
            )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user == comment.user or request.user == comment.post.author:
            return super().destroy(request, *args, **kwargs)
        return Response({'detail': 'Not allowed.'}, status=403)

#notification
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    try:
        notif = Notification.objects.get(id=pk, recipient=request.user)
        notif.is_read = True
        notif.save()
        return Response({"status": "marked as read"})
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=404)
    

