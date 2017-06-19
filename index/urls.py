from django.conf.urls import url

from . import views

app_name = 'index'

urlpatterns = [
    # hompage
    url(r'^$', views.index, name='index'),

    # redirect to results
    url(r'^(?P<question_text>\w+)/$', views.detail, name='detail'),

    # redirect to results and mark as student
    url(r'^(?P<question_text>\w+)/student$', views.student, name='student'),

]
