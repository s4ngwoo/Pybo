from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    post an answer to pybo.
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST': # when the request is 'POST'.
        # `request.POST` contains user input.
        form = AnswerForm(request.POST)
        if form.is_valid(): 
            # if the values of `subject`, and `content` is not valid,
            # form saves error message. 
            # And render question posting page again.
            answer = form.save(commit=False) 
            # save the form temporary to add `create_date` 
            # and asign it to `question`.
            # else, `create_date` not exist error will occur.
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save() # actual save. 
            return redirect('{}#answer_{}'.format(
                            resolve_url('pybo:detail', 
                                        question_id=question.id), 
                            answer.id))
    else: # when a request has been through a link.
        #return HttpResponseNotAllowed('Only POST is possible.') 
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False) 
            answer.modify_date = timezone.now() 
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', 
                            question_id=answer.question.id),
                answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer,
               'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        meesages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', 
                    question_id=answer.question.id),
        answer.id))
