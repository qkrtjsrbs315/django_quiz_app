# from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import UserInfo, Choice, Category
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.hashers import check_password, make_password  # 비밀번호 암호화 / 패스워드 체크
# from django.views.generic import View
# from django.core.paginator import Paginator

# Create your views here.
from django.views import View

def what(request):
    return render(request, 'what.html')
def index(request):
    return render(request, 'index.html')


def rank(request):
    username = UserInfo.objects.all().order_by('-score')
    #rank라는 필드에 인덱스 값을 넣어준다?
    cnt = 1
    for user in username:
        user.rank = cnt
        user.save
        cnt+=1
    return render(request, 'ranking.html',{'username':username})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        user = UserInfo.objects.all()
        print(user)
        username = request.POST.get('username')
        userid = request.POST.get('userid')
        userpw = request.POST.get('userpw')
        repw = request.POST.get('repw')
        if userpw != repw:
            return HttpResponse('<script>alert("아이디 또는 비밀번호가 일치하지않습니다!");location.replace(window.location.href)</script>')
        user = UserInfo.objects.create(username=username, userid=userid, userpw=userpw)
        user.save()
    return redirect('login')


class login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        id = request.POST.get('userid')
        pw = request.POST.get('userpw')
        print(id)
        print(pw)
        infos = UserInfo.objects.all()
        try:
            for infos in infos:
                if infos.userid == id and infos.userpw == pw:
                    print(infos)
                    name = infos.username
                    print(name)
                    request.session['username'] = name
                    return redirect('list')
        except ObjectDoesNotExist:
            return HttpResponse(
                '<script>alert("아이디 또는 비밀번호가 일치하지않습니다!");location.replace(window.location.href)</script>')


def quiz_list(request):
    all = Choice.objects.all()
    return render(request, 'list.html', {'all' : all})


def quiz_detail(request, id):
    username = request.session['username']
    print(username)
    request.session['score'] = 0
    user = UserInfo.objects.get(username=username)
    score = 0
    option1 = request.POST.get('option1')
    option2 = request.POST.get('option2')
    option3 = request.POST.get('option3')
    option4 = request.POST.get('option4')
    try:
        choice = Choice.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('rank')
    next = choice.id + 1
    if option1 == choice.answer or option2 == choice.answer or option3 == choice.answer or option4 == choice.answer:
        score += choice.score
        print(score)
        print("맞았습니다.")
    print(choice.score)
    print(user)
    print(user.score)

    user.score += score
    user.save()

    return render(request, 'detail.html', {'choice': choice, 'next': next, "username": username})