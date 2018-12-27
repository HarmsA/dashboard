from django.shortcuts import render, redirect
from .models import User, Comment, Message
from apps.books.models import Book, Author, Review
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages


# ------- LOGIN - CREATE USER - NO ADMIN-----------------------
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
        request.session['user_id']=user.id
    return redirect('users:dashboard')


# --------- DASHBOARD - COMMENTS- POSTS -------------------
def dashboard(request):
    if 'user_id' in request.session:
        users = User.objects.all()
        user = User.objects.get(id=request.session['user_id'])
        # print(Book.objects.filter())
        print('image', user.image)
        books = Book.objects.filter(book_reviews__user__id=request.session['user_id'])

        context = {
            'users':users,
            'logged_in_user':user,
            'title':'Users',
            'books':books
        }
        user = User.objects.get(id=request.session['user_id'])
        if user.admin:
            return redirect('users:admin')
        return render(request, 'users/dashboard.html', context)
    return redirect('users:login')

def show(request, user_id):
    writee = User.objects.get(id=user_id)
    writer = User.objects.get(id=request.session['user_id'])
    # books = Books.objects.filter()
    m = Message.objects.filter(writee=writee)
    n=Comment.objects.all()
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
        # print(m.writee.id)
        # writer_id = User.objects.filter(id=m.writee.id)
    else:
        return redirect('users:show', to_user_id)
    return redirect('users:show', m.writee_id)

def comment(request, to_user_id):
    comment = Comment.objects.v_comment(request.POST)
    if comment:
        user = User.objects.get(id=request.session['user_id'])
        c = Comment.objects.create_comment(request.POST, user)
        print(c.writee.id)
        print(c.writee.writee_id)
    else:
        return redirect('users:show', to_user_id)

    return redirect('users:show', c.writee.writee_id)

def search(request):
    try:
        book = Book.objects.get(title=request.POST['search'])
        return redirect('books:add_review', book.id)
    except:
        try:
            author = Author.objects.get(name=request.POST['search'])
            return redirect('books:authors_books', author.id )
        except:
            error = 'No such name or book exist, spacing and puncuation is required to be the same.'
            messages.error(request, error)
            return redirect('books:add_book')

# --------USER EDIT/UPDATE/VIEW-------------------------------------
def edit_profile(request):
    errors = User.objects.v_profile_change(request.POST, request.session['user_id'])
    if errors[0]:
        for error in errors[0]:
            messages.error(request, error)
        return redirect('users:profile')
    return redirect('users:dashboard')

def edit_password(request):
    errors = User.objects.v_password_change(request.POST, request.session['user_id'])
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:profile')
    return redirect('users:dashboard')

def edit_description(request):
    errors = User.objects.v_description_change(request.POST, request.session['user_id'])
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:profile')
    return redirect('users:dashboard')

def profile(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, 'users/edit.html', context)

# def add_image(request):
#     form = request.DATA
#     print(form)
#     return redirect('users:dashboard')

# --------LOGOUT - DELETE ------------------------------------------
def logout(request):
    request.session.clear()
    return redirect('users:login')

def delete_user(request, delete_user_id):
    user = User.objects.get(id=delete_user_id)
    user.delete()
    return redirect('users:admin')


# ----------ADMIN AREA-------------------------------------
def admin(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'Admin Users'
    }
    return render(request, 'users/admin.html', context)

def admin_edit(request, edit_user_id):
    user = User.objects.get(id=edit_user_id)
    context = {
        'user': user
    }
    return render(request, 'users/admin_edit.html', context)

def admin_edit_profile(request, edit_user_id):
    errors = User.objects.admin_edit_profile(request.POST, edit_user_id)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:admin_edit', edit_user_id)
    return redirect('users:dashboard')

def admin_edit_password(request, edit_user_id):
    print(request.POST)
    print('8'*80)
    errors = User.objects.v_password_change(request.POST, edit_user_id)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:admin_edit', edit_user_id)
    return redirect('users:dashboard')

def add_user(request):
    admin = User.objects.get(id=request.session['user_id'])
    if admin:
        context = {
            'title':'Add User'
        }
        return render(request, 'users/admin_add.html', context)
    return redirect('users:dashboard')

def admin_register_process(request):
    errors = User.objects.v_register(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('users:add_user')
    else:
        User.objects.admin_register(request.POST)
    return redirect('users:admin')
# --------------------------------------------------------------