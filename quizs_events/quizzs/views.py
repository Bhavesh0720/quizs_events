from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        msg = ""
        try:
            User.objects.get(email=email)
            msg = "this email exist use another!"
        except User.DoesNotExist:
            if password == confirm_password:
                User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                )
                return redirect('signin')
            else:
                msg = "password and confirm password must match!"
        con = {
            'msg':msg,
        }
        return render(request, 'signup.html', con)
    
    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        msg = ""
        try:
            user = User.objects.get(email=email)
            if password == user.password:
                request.session['uid'] = user.id
                return redirect('home')
            else:
                msg = "wrong password!"
        except User.DoesNotExist:
            msg = "this email is not registered!"
        
        con = {
            'msg':msg
        }
        return render(request, 'signin.html', con)
    
    return render(request, 'signin.html')


def home(request):
    return render(request, 'home.html')


def events(request):
    events = Event.objects.all()
    con = {
        'events':events,
    }
    return render(request, 'events.html', con)


def quiz_list(request):
    quizzs = Quiz.objects.all()
    con = {
        'quizzs':quizzs,
    }
    return render(request, 'quiz_list.html', con)


def quiz_attempt(request, quiz_id):
    if 'uid' not in request.session:
        return redirect('signin')
    
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)  
    quizzs = Quiz.objects.get(id=quiz_id)
    questions = quizzs.question.all().prefetch_related('answer')
    con = {
        'quizzs':quizzs,
        'questions':questions,
        'username':user.username,
    }
    return render(request, 'quiz_attempt.html', con)


def result(request):
    return render(request, 'result.html')


def signout(request):
    request.session.flush()
    return redirect('signin')