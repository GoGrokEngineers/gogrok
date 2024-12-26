from django.urls import path
from .views import CompetitionAPIView, JoinCompetitionView, SubmitCodeView, StatisticsAPIView

urlpatterns = [
    path('', CompetitionAPIView.as_view(), name='create-get-competition'),
    path('join/', JoinCompetitionView.as_view(), name='join-competition'),
    path('submit/', SubmitCodeView.as_view(), name='submit-code'),
    path('results/', StatisticsAPIView.as_view(), name='statistics' )
]
