from django.urls import path
from . import views
from .views import ProblemDetailView, ProblemListView, ProblemCreateView, ProblemUpdateView, SubmissionCreateView, SubmissionDetailView, SubmissionListView

urlpatterns = [
    path('', views.home, name='seer-home'),
    path('problems', ProblemListView.as_view(), name='problem-list'),
    path('problems/new/', ProblemCreateView.as_view(), name='problem-create'),
    path('problems/<int:pk>/update/', ProblemUpdateView.as_view(), name='problem-update'),
    path('problems/<int:pk>/submit/', SubmissionCreateView.as_view(), name="problem-submit"),
    path('about/', views.about, name='seer-about'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-detail'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail')
]