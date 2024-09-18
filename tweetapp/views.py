from django.shortcuts import render
from .models import Tweet, Comment, Like
from .forms import TweetForm, UserRegistration,User,CommentForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets =  Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {
        'tweets': tweets
    })


def search_tweet_list(request):
    query = request.GET.get('search', '')
    if query:
        # Find users whose username contains the search query
        users = User.objects.filter(username__icontains=query)
        # Get tweets from those users
        tweets = Tweet.objects.filter(user__in=users).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'search_query': query
    })



@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html',{
        'form': form
    })

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html',{
        'form': form
    })

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {
            'tweet': tweet
            })

def register(request):
    if request.method  == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistration()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def comment_create(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_list')
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {
        'form': form,
        'tweet': tweet
    })

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
    return redirect('tweet_list')
