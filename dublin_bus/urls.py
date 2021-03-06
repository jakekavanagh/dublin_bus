from django.conf.urls import url
from index import views
from django.views.generic.base import RedirectView


app_name = 'index'
favicon_view = RedirectView.as_view(url="{% static 'index/favicon.ico' %}", permanent=True)


urlpatterns = [
    # hompage
    url(r'^$', views.index, name='index'),

    url(r'^detail/$', views.detail, name='detail'),

    url(r'^find/$', views.find, name='find'),

    url(r'^find/detail/$', views.detail, name='find_detail'),

    url(r'^luas/$', views.luas, name='luas'),

    url(r'^favicon\.ico$', favicon_view),


    # redirect to results
    # url(r'^(?P<title>.*)/$', views.detail, name='detail'),

    # redirect to results and mark as student
    # url(r'^(?P<title>.*)/student$', views.student, name='student'),

]