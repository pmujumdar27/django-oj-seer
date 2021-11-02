from typing import List
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import ProblemFilter, SubmissionFilter

from seer.models import Problem, Submission

# Create your views here.

class ProblemListView(ListView):
    model = Problem
    template_name = 'seer/problems.html'
    context_object_name = 'problems'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProblemFilter(self.request.GET, queryset=self.get_queryset())
        return context

class ProblemDetailView(DetailView):
    model = Problem

class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem

    fields = [
        'title',
        'statement',
        'sample_input',
        'sample_output',
        'input_constraints',
        'rating',
        'test_inputs',
        'test_outputs',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('problem-list')

class ProblemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Problem

    fields = [
        'title',
        'statement',
        'sample_input',
        'sample_output',
        'input_constraints',
        'rating',
        'test_inputs',
        'test_outputs',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        problem = self.get_object()
        if self.request.user == problem.author:
            return True
        return False

    def get_success_url(self):
        return reverse('problem-list')

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission

    fields = ['code', 'language']

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.problem_id = get_object_or_404(Problem, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        # print(self.get_object())
        return reverse('submission-list')

class SubmissionDetailView(DetailView):
    model = Submission

class SubmissionListView(ListView):
    model = Submission
    context_object_name = 'submissions'
    ordering = ['-submit_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SubmissionFilter(self.request.GET, queryset=self.get_queryset())
        return context

def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'seer/home.html', context=context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'seer/about.html', context=context)