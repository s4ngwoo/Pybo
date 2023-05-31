from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST': # when the request is 'POST'.
        # `request.POST` contains user input.
        form = QuestionForm(request.POST)
        if form.is_valid(): 
            # if the values of `subject`, and `content` is not valid,
            # form saves error message. 
            # And render question posting page again.
            question = form.save(commit=False) 
            # save the form temporary to add `create_date` 
            # and asign it to `question`.
            # else, `create_date` not exist error will occur.
            question.author = request.user
            question.create_date = timezone.now()
            question.save() # actual save. 
            return redirect('pybo:index')
    else: # when a request has been through a link.
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) 
            question.modify_date = timezone.now() 
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)
