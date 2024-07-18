from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView
from .models import QuizCategories, QuestionModel
import random


class QuizCategoriesListView(ListView):
    model = QuizCategories
    template_name = "categories/index.html"
    
    queryset = QuizCategories.objects.all()

class QuestionListView(ListView):
    model = QuestionModel
    template_name = "quizzes/quizzes.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['pk']
        quiz_category = get_object_or_404(QuizCategories, category=category)
        context["quiz_category"] = quiz_category
        context["category_id"] = category
        return context
    
    def get_queryset(self):
        category = self.kwargs['pk']
        quiz_category = get_object_or_404(QuizCategories, category=category)
        return QuestionModel.objects.filter(question_category_id=category_id)


def home(request, category_id, question_id=None):
    request.session.setdefault('score', 0)
    request.session.setdefault('correct', 0)
    request.session.setdefault('wrong', 0)
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        question_id = request.POST.get('question_id')
        question = get_object_or_404(QuestionModel, id=question_id)
        user_answer = request.POST.get('answer')
        # Check if user's answer is correct
        if user_answer == question.answer:
            request.session['score'] = request.session.get('score', 0) + 10
            request.session['correct'] = request.session.get('correct', 0) + 1
        else:
            request.session['wrong'] = request.session.get('wrong', 0) + 1
        request.session.save()
        # Get the next question
        next_question = QuestionModel.objects.filter(question_category_id=category_id, id__gt=question_id).first()
        
        if next_question:
            return redirect('home', category_id=category_id, question_id=next_question.id)
        else:
            # If no next question, calculate final score
            total_questions = QuestionModel.objects.filter(question_category_id=category_id).count()
            percent = (request.session['score'] / (total_questions * 10)) * 100
            context = {
                'score': request.session['score'],
                'time': request.POST.get('timer'),
                'correct': request.session['correct'],
                'wrong': request.session['wrong'],
                'percent': percent,
                'total': total_questions
            }
            # Clear session data
            request.session['score'] = 0
            request.session['correct'] = 0
            request.session['wrong'] = 0
            request.session.save()
            return render(request, 'results/result.html', context)
    else:
        request.session.save()
        # Retrieve questions for the category
        questions = QuestionModel.objects.filter(question_category_id=category_id)
        
        if question_id is None:
            # If no question ID provided, start with the first question
            question = questions.first()
        else:
            # Otherwise, get the specified question
            question = get_object_or_404(QuestionModel, id=question_id)
        
        # Shuffle answer options
        answers = [question.option_01, question.option_02, question.option_03, question.option_04]
        random.shuffle(answers)
        
        # Find the next question's ID
        next_question = questions.filter(id__gt=question.id).first()
        next_question_id = next_question.id if next_question else None
        
        # Prepare context for rendering the template
        context = {
            'question': question,
            'answers': answers,
            'category_id': category_id,
            'question_id': question.id,
            'next_question_id': next_question_id
        }
        
        # Render the quiz template
        return render(request, 'quizzes/quizzes.html', context)
    