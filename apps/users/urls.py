from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login_process/$', views.login_process, name='login_process'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_process/$', views.register_process, name='register_process'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^show/(?P<user_id>\d+)/$', views.show, name='show'),
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^message/(?P<to_user_id>\d+)/$', views.message, name='message'),
    url(r'^comment/(?P<to_user_id>\d+)/$', views.comment, name='comment'),
    url(r'^search/$', views.search, name='search'),

    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_password/$', views.edit_password, name='edit_password'),
    url(r'^edit_description/$', views.edit_description, name='edit_description'),
    url(r'^delete_user/(?P<delete_user_id>\d+)/$', views.delete_user, name='delete_user'),

    url(r'^admin/$', views.admin, name='admin'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^admin_register_process/$', views.admin_register_process, name='admin_register_process'),
    url(r'^admin_edit/(?P<edit_user_id>\d+)/$', views.admin_edit, name='admin_edit'),
    url(r'^admin_edit_profile/(?P<edit_user_id>\d+)/$', views.admin_edit_profile, name='admin_edit_profile'),
    url(r'^admin_edit_password/(?P<edit_user_id>\d+)/$', views.admin_edit_password, name='admin_edit_password'),
    # url(r'^comment/$', views.comment, name='comment'),
]
