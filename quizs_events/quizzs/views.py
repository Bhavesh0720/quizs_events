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
    # only signin user can attempt!
    if 'uid' not in request.session:
        return redirect('signin')
    
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)  
    quiz = Quiz.objects.get(id=quiz_id)

    # ans related to que and que related to quiz
    questions = quiz.question.all().prefetch_related('answer')  

    if request.method == "POST":
        user_name = request.POST.get('user_name')
        score = 0

        submission = UserSubmission.objects.create(
            quiz = quiz,
            user_name = user_name,
            score = score
        )

        for qs in questions:
            # user selected ans_ids in a list 
            selected_ids = request.POST.getlist(f"q_{qs.id}")
            selected_ids = [int(x) for x in selected_ids]

            # correct ans_ids 
            correct_ids = list(qs.answer.filter(is_correct=True).values_list('id', flat=True))

            for ans_id in selected_ids:
                ans = Answer.objects.get(id=ans_id)
                UserAnswer.objects.create(
                    submission=submission,
                    question=qs,
                    answer=ans.text,
                    is_correct=ans.is_correct
                )
            
            # update score only if all selected answer is correct for a multilpe type question 
            if set(selected_ids) == set(correct_ids):
                score += 1
        
        submission.score = score
        submission.save()

        return redirect('result', submission_id=submission.id)

    con = {
        'quiz':quiz,
        'questions':questions,
        'user_name':user.username,
    }
    return render(request, 'quiz_attempt.html', con)


def result(request, submission_id):
    submission = UserSubmission.objects.get(id=submission_id)
    user_answers = submission.user_answer.select_related('question').all()

    grouped = {}

    for ua in user_answers:
        qs = ua.question
        if qs.id not in grouped:
            grouped[qs.id]={
                "question":qs,
                "user_ans":[],
                "correct_ans":list(qs.answer.filter(is_correct=True).values_list('text', flat=True))                
            }

        grouped[qs.id]["user_ans"].append({
            "text":ua.answer,
            "is_correct":ua.is_correct
        })    

    results = []
    for val in grouped.values():
        # fileter correct user ans
        user_correct = [x["text"] for x in val["user_ans"] if x["is_correct"] ]

        # only correct if all multiple choice ans is correct
        fully_correct = set(user_correct) == set(val["correct_ans"])

        results.append({
            "question":val["question"],
            "user_answers":val["user_ans"],
            "correct_answers":val["correct_ans"],
            "is_correct":fully_correct
        })


    con = {
        'submission':submission,
        'results':results,
    }
    return render(request, 'result.html', con)


def quiz_history(request):
    if 'uid' not in request.session:
        return redirect('signin')
    
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    submission = UserSubmission.objects.filter(user_name=user.username)

    con = {
        'submission':submission,
        'username':user.username,
    }

    return render(request, 'quiz_history.html', con)


def signout(request):
    request.session.flush()
    return redirect('signin')