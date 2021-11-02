import django_filters
from .models import Problem, Submission

class ProblemFilter(django_filters.FilterSet):

    class Meta:
        model = Problem
        fields = ['title', 'author', 'rating']

class SubmissionFilter(django_filters.FilterSet):

    class Meta:
        model = Submission
        fields = ['problem_id', 'user_id', 'language', 'status']