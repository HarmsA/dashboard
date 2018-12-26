
from django.db import models
from apps.users.models import User

class AuthorManager(models.Manager):
    def create_author(self, form, context):
        create_author = Author.objects.create(
            name=context['author'],
        )
        return create_author

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()


class BookManager(models.Manager):
    def validate_book(self, form):
        errors = []
        if len(form['title'])<1:
            errors.append("Please enter a book name")
        if form['author']=='none' and len(form['new_author'])<1:
            errors.append("Please enter an authors name.")
        if len(form['description'])<2:
            errors.append("Please enter a valid review")
        return errors

    def create_book(self, form, context, author):
        user = User.objects.get(id=context['user_id'])

        created_book = Book.objects.create(
            title=form['title'],
            rating=form['rating'],
            author=author.Uppercase(),
            user=user
        )
        return created_book


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    user = models.ForeignKey(User, related_name='books')
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class ReviewManager(models.Manager):
    def validate_review(self, form):
        errors = []
        if len(form['description'])<5:
            errors.append('Description of must be a bit longer.')
        return errors

    def create_review(self, form, book, context):
        # book = Book.objects.get(id=form['bookid'])
        user = User.objects.get(id=context['user_id'])
        create_review = Review.objects.create(
            description=form['description'],
            user=user,
            book=book,
        )
        return create_review

class Review(models.Model):
    description = models.TextField(default='None')
    user = models.ForeignKey(User, related_name='user_reviews')
    book = models.ForeignKey(Book, related_name='book_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    def __str__(self):
        return self.description
