from django.shortcuts import render, get_object_or_404
from .models import Question, EventApi
from .apps import IndexConfig

from django.views.generic.edit import CreateView, UpdateView



def index(request):
    df = ([[41.409092, 10.0, 33.0, 227.0,0.0, 13.0, 0.0, 2.0,16.0]])
    all_questions = Question.objects.all()
    all_events = EventApi.objects.all()
    x = IndexConfig.y
    val = x.predict(df)
    y = "hi"
    print(type(val))
    context = {
        'all_questions': all_questions,
        'all_events': all_events,
        'val': y,
               }
    return render(request, 'index/index.html', context)


def detail(request, title):
    """ the below line of code is a Django shortcut for raising a 404 error if the
    variable does not exist in the database without using try except"""
    event = get_object_or_404(EventApi, title=title)
    return render(request, "index/detail.html", {"event": event})


def student(request, question_text):
    question = get_object_or_404(Question, question_text=question_text)
    selected = request.POST["student"]
    context = {
        "question": question,
        "selected": selected
    }
    return render(request, "detail/detail.html", context)
