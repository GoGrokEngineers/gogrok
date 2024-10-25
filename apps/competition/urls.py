from django.urls import path
from .views import CompetitionCreateView, JoinCompetitionView

urlpatterns = [
    path('create/', CompetitionCreateView.as_view(), name='create-competition'),
    path('join/', JoinCompetitionView.as_view(), name='join-competition')
]
