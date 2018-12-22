from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_process/$', views.login_process, name='login_process'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_process/$', views.register_process, name='register_process'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^show/(?P<user_id>\d+)/$', views.show, name='show'),
    url(r'^message/(?P<to_user_id>\d+)/$', views.message, name='message'),
    url(r'^comment/(?P<to_user_id>\d+)/$', views.comment, name='comment'),
    # url(r'^comment/$', views.comment, name='comment'),
]
