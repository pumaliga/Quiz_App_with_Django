from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Quiz, Question, Answer


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "topic", "number_of_questions", "time", "required_score_to_pass", "difficulty"]


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["text", "quiz"]


class AnswersForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "correct", "question"]