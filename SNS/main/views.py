from django.shortcuts import render,get_object_or_404,redirect
from .models import Message,Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden


###@login_requiredの内容
##if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
##        return redirect('account_login')



#userIDからuserオブジェクトを返す
def user_create(get_id):
    User = get_user_model()
    user = User.objects.get(id=get_id)
    return user



#メインページ
def msg_list(request):
    msg = Message.objects.all().order_by('-date_created')
    for text in msg:
        text.likes = text.liked_by.count()
        text.comments = text.commented_by.count()
        if request.user.is_authenticated:

            if text.liked_by.filter(id=request.user.id).exists():#いいねしていない場合
                text.liked=True
            else:
                text.liked=False

        else:
            text.liked=False

    paginator = Paginator(msg, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/msg_list.html', {'msg': page_obj})



#投稿ページを表示
@login_required
def post_page(request):
        return render(request,'post/post_page.html')



#投稿内容を送信
@login_required
def msg_post(request):
    Message.objects.create(msg_text=request.POST.get("msg_text"),
                             user = user_create(request.user.id)
                             )
    return redirect('msg_list')



#マイページを表示
@login_required
def my_page(request):
    msg = Message.objects.filter(user=request.user).order_by('-date_created')
    for text in msg:
        text.likes = text.liked_by.count()
        text.comments = text.commented_by.count()
        if request.user.is_authenticated:

            if text.liked_by.filter(id=request.user.id).exists():#いいねしていない場合
                text.liked=True
            else:
                text.liked=False

        else:
            text.liked=False

    user= get_object_or_404(get_user_model(), id=request.user.id)
    followers=user.followers.all().count()
    follows=user.following.all().count()

    return render(request, 'main/my_page.html', {'msg':msg,'followers':followers,'follows':follows})



#goodを管理
@login_required
def get_likes(request,pk):
    post = get_object_or_404(Message, pk=pk)
    liked = False
    if post.liked_by.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        if 'like' or 'unlike'in request.POST:
            if liked:
                post.liked_by.remove(request.user)
            else:
                post.liked_by.add(request.user)
            return redirect('msg_list')
    return render(request, 'msg_list.html', {'post': post, 'liked': liked})



#コメントページを表示
@login_required
def comment_page(request,pk):
    target = get_object_or_404(Message, pk=pk)
    comments_list = target.commented_by.all()
    return render(request, 'comment/comment_page.html', {'target':target,'comments_list':comments_list})



#コメントを送信
@login_required
def get_comments(request,pk):
    comment = Comment.objects.create(comment_text=request.POST.get("comment_text"),
                                     user = user_create(request.user.id)
                                     )

    post = get_object_or_404(Message, pk=pk)
    post.commented_by.add(comment)
    return redirect('msg_list')



#フォロー機能
@login_required
def follow_post(request,pk): #pkの内容はフォローするターゲットのユーザーID
    post = get_object_or_404(get_user_model(), pk=request.user.id)
    followed = False
    if post.following.filter(id=pk).exists():#ログイン中のユーザーのフォローリストにターゲットがいない場合
        followed = True
    if request.method == 'POST':
        if 'follow' in request.POST:
            if followed:#フォローしていた場合
                post.following.remove(user_create(pk))
            else:
                post.following.add(user_create(pk))
    return redirect('user_page',pk=pk)


#ユーザーページ
#@login_required
def user_page(request,pk):
    user= get_object_or_404(get_user_model(), pk=pk)
    msg = Message.objects.filter(user=user).order_by('-date_created')
    for text in msg:
        text.likes = text.liked_by.count()
        text.comments = text.commented_by.count()
        if request.user.is_authenticated:

            if text.liked_by.filter(id=request.user.id).exists():#いいねしていない場合
                text.liked=True
            else:
                text.liked=False

        else:
            text.liked=False


    if request.user.is_authenticated:
            if request.user.following.filter(pk=pk).exists():#フォローしていない場合
                followed = True
            else:
                followed = False
    else:
        followed = False

    followers=user.followers.all().count()
    follows=user.following.all().count()

    return render(request, 'main/user_page.html', {'followed':followed,'follows':follows,'followers':followers,'users':user,'msg':msg})

#マイページのフォロー中のユーザー
@login_required
def follows(request):
    user= get_object_or_404(get_user_model(), id=request.user.id)
    follows=user.following.all()
    return render(request, 'main/follows.html', {'follows':follows})

#マイページのフォローされているユーザー
@login_required
def followers(request):
    user= get_object_or_404(get_user_model(), id=request.user.id)
    followers=user.followers.all()
    return render(request, 'main/followers.html', {'followers':followers})

#ユーザーページのフォロー中のユーザー
@login_required
def user_follows(request,pk):
    user= get_object_or_404(get_user_model(), pk=pk)
    follows=user.following.all()
    return render(request, 'main/follows.html', {'follows':follows})

#ユーザーページのフォローされているユーザー
@login_required
def user_followers(request,pk):
    user= get_object_or_404(get_user_model(), pk=pk)
    followers=user.followers.all()
    return render(request, 'main/followers.html', {'followers':followers})

#マイページのメッセージの削除
@login_required
def msg_delete(request,pk): 
    msg = Message.objects.get(pk=pk)
    if msg.user.id==request.user.id:
        msg.delete()
        return redirect('my_page')
    else:
        return HttpResponseForbidden()
