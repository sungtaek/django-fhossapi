from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth-token/$', views.AuthToken.as_view()),
    url(r'^user/$', views.UserSearchView.as_view()),
    url(r'^user/(?P<name>[:0-9A-Za-z_\-\.@]+)/$', views.UserDetailView.as_view()),
    url(r'^service/$', views.ServiceSearchView.as_view()),
    url(r'^service/(?P<identity>[0-9]+)/$', views.ServiceDetailView.as_view()),
]
