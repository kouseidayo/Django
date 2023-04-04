from django.shortcuts import render
from .models import Message,Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


###@login_requiredの内容
##if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
##        return redirect('account_login')



#userIDからuserオブジェクトを返す
def user_create(get_id):
    User = get_user_model()
    user = User.objects.get(id=get_id)
    return user



#メインページ
#@login_required                 $$$$$$$$$$$$$$未ログイン中はエラーになってしまう
def msg_list(request):
    msg = Message.objects.all()
    for text in msg:
        text.likes = text.liked_by.count()
        if text.liked_by.filter(id=request.user.id).exists():#いいねしていない場合
            text.liked=True
        else:
            text.liked=False

        user = get_user_model().objects.get(id = text.user.id) #逆参照(仮)
        text.followers = user.followers.all().count()
        
        if request.user.following.filter(id=text.user.id).exists():#フォローしていない場合
            text.followed = True
        else:
            text.followed = False

    
    return render(request, 'main/msg_list.html', {'msg': msg})



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
    msg = Message.objects.filter(user=request.user)
    for text in msg:
        text.likes = text.liked_by.count()
        
    return render(request, 'main/my_page.html', {'msg':msg})



#goodを管理
@login_required  
def get_likes(request,pk):
    post = get_object_or_404(Message, pk=pk)
    liked = False
    if post.liked_by.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        if 'like' in request.POST:
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
    return redirect('msg_list')


    
