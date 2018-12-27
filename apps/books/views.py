from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users.models import User
from apps.books.models import Book, Review, Author

# Create your views here.
def books(request):
    if 'user_id' not in request.session:
        return redirect('users:login')
    user = User.objects.get(id=request.session['user_id'])
    print(user.f_name)
    review = Review.objects.filter()
    books = Book.objects.all()
    x=0
    for book in books:
        x+=1
    if x>4:
        x=x-2
    recent_books = Book.objects.all()[x::-1]

    context = {
        'f_name': user.f_name,
        'books': books,
        'first_three':recent_books,
    }
    print('8'*80)
    # print(user.user_reviews.all())
    return render(request, 'books/book_index.html', context)

def add_book(request):
    if 'user_id' not in request.session:
        return redirect('users:login')
    user = User.objects.get(id=request.session['user_id'])

    authors = Author.objects.all()
    books = Book.objects.all()

    context = {
        'user_id':user.id,
        'books': books,
        'authors':authors,
    }
    return render(request, 'books/add_book.html', context)

def add_review(request, book_id):
    if 'user_id' not in request.session:
        return redirect('users:login')
    review = Review.objects.filter(book__id=book_id)
    book = Book.objects.get(id=book_id)
    author = Author.objects.get(books__id=book.id)
    # review = Review.objects.get(book__id=book_id)
    user = User.objects.get(id=request.session['user_id'])

    context = {
        # 'edit':edit,
        'author':author,
        'title':book.title,
        'book':book.id,
        'reviews':review,
        'rating':book.rating,
        'user':user,
        'date':book.created_at,
    }

    return render(request, 'books/add_review.html', context)

# def add_book_review(request):
#     return render(request, 'book/add_book.html')


def validate_book_entry(request):
    errors = Book.objects.validate_book(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('books:add_book')
    # Checks to see if an existing author was selected, will use
    # by default, if none then new_author == author
    if request.POST['author'] == 'none':
        request.session['author'] = request.POST['new_author']
    else:
        request.session['author'] = request.POST['author']
    # user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_id':request.session['user_id'],
        'author':request.session['author']
    }

    try:
        author = Author.objects.get(name=context['author'])
    except:
        author = Author.objects.create_author(request.POST, context)
    book = Book.objects.create_book(request.POST, context, author)
    print(book)
    review = Review.objects.create_review(request.POST, book, context)
    return redirect('books:add_review', book.id)

def add(request):
    pass

def new_user_review(request, book_id):
    errors = Review.objects.validate_review(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('books:add_review', request.POST['bookid'])
    context = {
        'user_id':request.session['user_id'],
    }
    book = Book.objects.get(id=book_id)
    Review.objects.create_review(request.POST, book, context)
    return redirect('books:add_review', request.POST['bookid'])

def authors_books(request, author_id):
    books = Book.objects.filter(author_id=author_id)
    author = Author.objects.get(id=author_id)
    context = {
        'books':books,
        'author':author,
    }
    return render(request, 'books/authors_books.html', context)

def delete(request, review_id, book_id):
    deletion = Review.objects.get(id=review_id)
    deletion.delete()
    print(request.POST)
    return redirect('books:add_review', book_id)