from django.shortcuts import render, redirect
from .models import User, Comment, Message
from django.contrib import messages

# Create your views here.
def login(request):
    context = {
        'title':'Login'
    }
    return render(request, 'users/login.html', context)

def login_process(request):
    errors = User.objects.v_login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:login')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('users:dashboard')

def register(request):
    context = {
        'title':'Register'
    }
    return render(request, 'users/register.html', context)

def register_process(request):
    errors = User.objects.v_register(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:register')
    else:
        user = User.objects.register(request.POST)
        print('8'*80)
        print(user)
        request.session['user_id']=user.id
    return redirect('users:dashboard')

def dashboard(request):
    if 'user_id' in request.session:
        users = User.objects.all()
        context = {
            'users':users,
            'title':'Users'

        }
        return render(request, 'users/dashboard.html', context)
    return redirect('users:login')

def show(request, user_id):
    print(user_id)
    writee = User.objects.get(id=user_id)
    # print('8'*80)
    # print('writee = ',writee)
    writer = User.objects.get(id=request.session['user_id'])
    # print('writer = ', writer)
    m = Message.objects.filter(writee=writee)
    # print('m = ', m)
    n=Comment.objects.all()
    # print('n = ', n)
    context = {
        'user':writee,
        'writer':writer,
        'messages':m,
        'notes':n,
    }
    return render(request, 'users/show.html', context)

def message(request, to_user_id):
    message = Message.objects.v_message(request.POST)
    if message:
        user = User.objects.get(id=request.session['user_id'])
        m = Message.objects.create_message(request.POST, to_user_id, user)
        print(m.writee.id)
        writer_id = User.objects.filter(id=m.writee.id)
    return redirect('users:show', m.writee_id)

def comment(request, to_user_id):
    comment = Comment.objects.v_comment(request.POST)
    if comment:
        user = User.objects.get(id=request.session['user_id'])
        c = Comment.objects.create_comment(request.POST, user)
        print(c.writee.id)
        print(c.writee.writee_id)

    return redirect('users:show', c.writee.writee_id)
