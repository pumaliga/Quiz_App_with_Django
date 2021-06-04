from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from .forms import RegisterForm, QuizForm, QuestionForm, AnswersForm
from .models import Quiz, Question, Answer, Result
from django.views.generic import ListView, CreateView, DetailView
from django.http import JsonResponse


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = '/login/'


class QuizListView(ListView):
    model = Quiz
    template_name = 'main.html'


class QuizCreateView(CreateView):
    form_class = QuizForm
    success_url = '/'
    template_name = 'quiz_create.html'


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    success_url = '/question_create/'
    template_name = 'question_create.html'


class AnswersCreateView(CreateView):
    model = Answer
    form_class = AnswersForm
    success_url = '/answers/'
    template_name = 'answers.html'


class QuizDetailView(DetailView):
    # pk_url_kwarg = 'pk'
    model = Quiz
    template_name = 'quiz.html'

    def quiz_view(self, pk):
        quiz = Quiz.objects.get(pk=pk)
        return render(self, 'quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


