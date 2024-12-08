from django.urls import path
from .views import CompetitionCreateView, JoinCompetitionView
# SumbitCodeView, StatisticsAPIVIew


urlpatterns = [
    path('create/', CompetitionCreateView.as_view(), name='create-competition'),
    path('join/', JoinCompetitionView.as_view(), name='join-competition'),
    # path('submit/', SumbitCodeView.as_view(), name='submit-code'),
    # path('results/', StatisticsAPIVIew.as_view(), name='statistics' )
]
