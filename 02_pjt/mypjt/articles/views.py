from django.shortcuts import render, redirect
from accounts.models import User
from . import forms
from . import models
# Create your views here.
def index(request, pk):
    user = request.user
    articles = models.Articles.objects.all().filter(board_num = pk)
    context = {
        'user' : user,
        'articles' : articles,
        'pk' : pk,
    }
    return render(request, 'articles/index.html', context)

def upload(request):
    if request.method == 'POST':
        board_num = request.POST.get('board_num')
        comment = request.POST.get('comment')
        author = request.POST.get('author')
        print(comment, author)
        models.Articles.objects.create(comment=comment, author=author, rate=5, board_num=board_num)
        return redirect('articles:index', board_num)