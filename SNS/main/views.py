from django.shortcuts import render
from .models import Message
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required




def user_create(get_id):
    User = get_user_model()
    user = User.objects.get(id=get_id)
    return user

@login_required    
def msg_list(request):
    msg = Message.objects.all()
    for text in msg:
        text.likes = text.liked_by.count()
        if text.liked_by.filter(id=request.user.id).exists():
            text.liked=True
        else:
            text.liked=False
    
    return render(request, 'main/msg_list.html', {'msg': msg})


def post_page(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')
    
    return render(request,'post/post_page.html')


def msg_post(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')
    
    Message.objects.create(msg_text=request.POST.get("msg_text"),
                             #good=request.POST.get("good"),
                             user = user_create(request.user.id)
                             )

    return redirect('msg_list')

#https://teratail.com/questions/288797
def my_page(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')

    msg = Message.objects.filter(user=request.user)
    for text in msg:
        text.likes = text.liked_by.count()
        
    return render(request, 'main/my_page.html', {'msg':msg})


def get_likes(request,pk):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')
    
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

#djangoでgood機能の実装方法を教えて  bing

    
