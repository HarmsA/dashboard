from django.conf.urls import url
from apps.books import views

urlpatterns = [
    url(r'^$', views.books, name='books'),
    # url(r'^add/$', views.add, name='add'),
    url(r'^add_review/$', views.add_review, name='add_review'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^add_review/(?P<book_id>\d+)/$', views.add_review, name='add_review'),
    url(r'^validate_book_entry/$', views.validate_book_entry, name='validate_book_entry'),
    url(r'^new_user_review/(?P<book_id>\d+)/$', views.new_user_review, name='new_user_review'),
    url(r'^delete/(?P<review_id>\d+)/(?P<book_id>\d+)/$', views.delete, name='delete'),
]
