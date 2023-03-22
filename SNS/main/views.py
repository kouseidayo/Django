from django.shortcuts import render
from .models import Message
from django.shortcuts import redirect
from django.contrib.auth import get_user_model





def user_create(get_id):
    User = get_user_model()
    user = User.objects.get(id=get_id)
    return user
    
def msg_list(request):
##    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
##        return redirect('account_login')
    
    msg = Message.objects.all()
    return render(request, 'main/msg_list.html', {'msg':msg})


def post_page(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')
    
    return render(request,'post/post_page.html')


def msg_post(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')
    
    Message.objects.create(msg_text=request.POST.get("msg_text"),
                             good=request.POST.get("good"),
                             user = user_create(request.user.id)
                             )

    return redirect('msg_list')

#https://teratail.com/questions/288797
def my_page(request):
    if not request.user.is_authenticated: #未ログインはログインページにリダイレクト
        return redirect('account_login')

    msg = Message.objects.filter(user=request.user)
    return render(request, 'main/my_page.html', {'msg':msg})




#djangoでgood機能の実装方法を教えて  bing

    
