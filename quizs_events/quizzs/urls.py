
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('events', views.events, name='events'),
    path('quiz_list', views.quiz_list, name='quiz_list'),
    path('quiz_attempt/<int:quiz_id>', views.quiz_attempt, name='quiz_attempt'),
    path('result/<int:submission_id>', views.result, name='result'),
]
