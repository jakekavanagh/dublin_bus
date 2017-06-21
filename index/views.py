from django.shortcuts import render, get_object_or_404
from .models import Question, EventApi

from django.views.generic.edit import CreateView, UpdateView



def index(request):
    all_questions = Question.objects.all()
    all_events = EventApi.objects.all()
    context = {
        'all_questions': all_questions,
        'all_events': all_events,
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
