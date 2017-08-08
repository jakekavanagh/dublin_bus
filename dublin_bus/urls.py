from django.conf.urls import url
from index import views

app_name = 'index'

urlpatterns = [
    # hompage
    url(r'^$', views.index, name='index'),

    url(r'^detail/$', views.detail, name='detail'),

    url(r'^find/$', views.find, name='find'),

    url(r'^find/detail/$', views.detail, name='find_detail'),

    url(r'^indexmobile/$', views.indexmobile, name='indexmobile'),

    url(r'^luas/$', views.luas, name='luas'),


    # redirect to results
    # url(r'^(?P<title>.*)/$', views.detail, name='detail'),

    # redirect to results and mark as student
    # url(r'^(?P<title>.*)/student$', views.student, name='student'),

]