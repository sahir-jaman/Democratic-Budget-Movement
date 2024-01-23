from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category


# Create your views here.
def home(request):
    posts = Post.objects.filter(status='publish').order_by('-id')[:8]
    latest_feature_news = Post.objects.filter(category__name='feature_news').order_by('-id').first()
    latest_feature_column = Post.objects.filter(category__name='feature_column').order_by('-id').first()
    media = Post.objects.filter(category__name='media').order_by('-id')[:6]
    # Retrieve one post per category
    categories = Category.objects.exclude(name__in=['feature_news', 'feature_column', 'media', 'slider', 'draft']).order_by('-created_at')
    posts_per_category = []
    for category in categories:
        post = Post.objects.filter(category=category,status='publish').order_by('-created_at').first()
        if post:
            posts_per_category.append(post)
                

    context = {
        "posts": posts,
        "featureNews": latest_feature_news,
        "featureColumn": latest_feature_column,
        'media':media,
        "posts_per_category": posts_per_category,
    }
    return render(request, "home.html", context)

def postDetail(request, uid):
    if uid:
        obj = get_object_or_404(Post, uid=uid)
        related_posts = Post.objects.filter(category=obj.category).exclude(uid=obj.uid)
        return render(request, "blog_detail.html", {'blog': obj, 'related_posts': related_posts})
    else:
        # Handle the case where 'uid' is not provided (redirect, show an error, etc.)
        return HttpResponse("Invalid request")
    
def aboutPage(request):
    return render(request, "about.html")

def category_posts(request, obj):
    cat_posts = Post.objects.filter(category__name=obj).order_by('-id')
    return render(request, 'category_posts.html', {"cat_posts":cat_posts})

