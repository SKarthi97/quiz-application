from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuizCategoriesListView.as_view(), name="category-list"),
    path("category/<int:pk>/", views.QuestionListView.as_view(), name="quizzes-list"),
    path("quiz/<int:category_id>/<int:question_id>/", views.home, name="home"),
    path("quiz/<int:category_id>/", views.home, name="home-start"),  # Starting point of the quiz within a category
]