from django.db import models

class QuizCategories(models.Model):
    """docstring for QuizCollectionSet."""
    
    category = models.CharField(max_length=50, unique = True)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category

    
class QuestionModel(models.Model):
    """docstring for QuestionModel."""
    
    question = models.CharField(max_length=200, null=True)
    option_01 = models.CharField(max_length=200, null=True)
    option_02 = models.CharField(max_length=200, null=True)
    option_03 = models.CharField(max_length=200, null=True)
    option_04 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)
    question_category = models.ForeignKey(QuizCategories, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question
