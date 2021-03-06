from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from users.models import User
from users.forms import RegisterForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect('/user/login/')
        else:
            return render(request, 'register.html',{'error':form.errors})
    return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname').strip()
        password = request.POST.get('password').strip()
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html',{'error':'用户不存在'})
        if check_password(password,user.password):
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.icon.url
            return redirect('/user/info/')
        else:
            return render(request, 'login.html', {'error': '密码错误'})
    else:
        return render(request,'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(request,'user_info.html',{'user':user})




















