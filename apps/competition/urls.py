from django.urls import path
from .views import CompetitionCreateView, JoinCompetitionView, SubmitCodeView, StatisticsAPIView



urlpatterns = [
    path('create/', CompetitionCreateView.as_view(), name='create-competition'),
    path('join/', JoinCompetitionView.as_view(), name='join-competition'),
    path('submit/', SubmitCodeView.as_view(), name='submit-code'),
    path('results/', StatisticsAPIView.as_view(), name='statistics' )

]
