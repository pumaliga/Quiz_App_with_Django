from django.urls import path
from .views import QuizListView, QuizDetailView, quiz_data_view, save_quiz_view, Register, Login, Logout, QuizCreateView, \
    QuestionCreateView, AnswersCreateView

urlpatterns = [
    path('', QuizListView.as_view(), name='base'),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path('<pk>/quiz/', QuizDetailView.as_view(), name='quiz'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('quiz_create/', QuizCreateView.as_view(), name="quiz_create"),
    path('question_create/', QuestionCreateView.as_view(), name="question_create"),
    path('answers/', AnswersCreateView.as_view(), name="answers")
]
