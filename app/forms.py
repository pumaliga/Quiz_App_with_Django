from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Quiz, Question


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]


class QuizForm(ModelForm):
    class Meta:
        model: Quiz
        fields = ["__all__"]


class QuestionForm(ModelForm):
    class Meta:
        model: Question
        fields = ["__all__"]