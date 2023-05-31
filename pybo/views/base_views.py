from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from ..models import Question

# Create your views here.

def index(request):
    #return HttpResponse("Hi, Welcome to pybo!")
    page = request.GET.get('page', '1') # page
    kw = request.GET.get('kw', '') # get 'kw' if not return ''
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
                Q(subject__icontains=kw) | # '__' access to sub attr.
                Q(content__icontains=kw) | 
                # `icontains` consider letter case, 
                # `contains` does not consider letter case
                Q(answer__content__icontains=kw) |  
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw) 
                # Is username of author who answer the question in?
                # and care about letter case.
                ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,
               'page': page,
               'kw': kw}
    # `question_list` is paging object(page_obj)
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
