from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth-token/$', views.AuthToken.as_view()),
    url(r'^user/$', views.UserListView.as_view()),
    url(r'^user/_add$', views.UserAddView.as_view()),
    url(r'^user/(?P<identity>[:0-9A-Za-z_\-\.@]+)/$', views.UserView.as_view()),
    url(r'^service/$', views.ServiceList.as_view()),
    url(r'^service/_add$', views.ServiceAdd.as_view()),
    url(r'^service/(?P<identity>[0-9]+)/$', views.Service.as_view()),
]
