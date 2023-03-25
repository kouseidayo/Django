from django.shortcuts import render
from .models import Message,Comment
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

##if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
##        return redirect('account_login')


def user_create(get_id):
    User = get_user_model()
    user = User.objects.get(id=get_id)
    return user


#@login_required    
def msg_list(request):
    msg = Message.objects.all()
    for text in msg:
        text.likes = text.liked_by.count()
        if text.liked_by.filter(id=request.user.id).exists():
            text.liked=True
        else:
            text.liked=False
    
    return render(request, 'main/msg_list.html', {'msg': msg})


@login_required  
def post_page(request):
        return render(request,'post/post_page.html')


@login_required  
def msg_post(request):
    Message.objects.create(msg_text=request.POST.get("msg_text"),
                             user = user_create(request.user.id)
                             )
    return redirect('msg_list')


@login_required  
def my_page(request):
    msg = Message.objects.filter(user=request.user)
    for text in msg:
        text.likes = text.liked_by.count()
        
    return render(request, 'main/my_page.html', {'msg':msg})


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


@login_required
def comment_page(request,pk):
    target = get_object_or_404(Message, pk=pk)
    comments_list = target.commented_by.all()
    return render(request, 'comment/comment_page.html', {'target':target,'comments_list':comments_list})

    
@login_required  
def get_comments(request,pk):
    comment = Comment.objects.create(comment_text=request.POST.get("comment_text"),
                                     user = user_create(request.user.id)
                                     )

    post = get_object_or_404(Message, pk=pk)
    post.commented_by.add(comment)
    return redirect('msg_list')



    
