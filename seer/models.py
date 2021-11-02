from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [('C++', 'C++'), ('C','C'), ('Python','Python'), ('Java','Java')]
STATUS_CHOICES = [('In Queue','In Queue'), ('Running','Running'), ('WA','WA'), ('TLE','TLE'), ('Accepted','Accepted')]

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    statement = models.TextField(null=True, blank=True)
    sample_input = models.TextField(null=True, blank=True)
    sample_output = models.TextField(null=True, blank=True)
    input_constraints = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    test_inputs = models.FileField(null=True, blank=True, upload_to="inputs/")
    test_outputs = models.FileField(null=True, blank=True, upload_to="outputs/")

    def __str__(self):
        return f'Problem: {self.title}'

class Submission(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=31, choices=LANGUAGE_CHOICES, null=True)
    status = models.CharField(max_length=31, choices=STATUS_CHOICES, default='In Queue')
    submit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Submission: {self.id} for Problem {self.problem_id}'