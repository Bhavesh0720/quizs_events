from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.TextField()

    def __str__(self):
        return self.title
    

class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Question(models.Model):
    QUESTION_TYPE=[
        ("SINGLE", "SINGLE"),
        ("MULTIPLE", "MULTIPLE")
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    text = models.TextField()
    question_type = models.CharField(choices=QUESTION_TYPE, default="SINGLE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text + " : " + self.quiz.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text