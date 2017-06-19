from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    all_questions = Question.objects.all()
    context = {'all_questions': all_questions}
    return render(request, 'index/index.html', context)


def detail(request, question_text):
    """ the below line of code is a Django shortcut for raising a 404 error if the
    variable does not exist in the database without using try except"""
    question = get_object_or_404(Question, question_text=question_text)
    return render(request, "detail/detail.html", {"question": question})


def student(request, question_text):
    question = get_object_or_404(Question, question_text=question_text)
    selected = request.POST["student"]
    context = {
        "question": question,
        "selected": selected
    }
    return render(request, "detail/detail.html", context)
