from django.urls import path
<<<<<<< HEAD
from .views import CompetitionCreateView, JoinCompetitionView
# SumbitCodeView, StatisticsAPIVIew
=======
from .views import CompetitionCreateView, JoinCompetitionView, SubmitCodeView, StatisticsAPIView
>>>>>>> origin/main


urlpatterns = [
    path('create/', CompetitionCreateView.as_view(), name='create-competition'),
    path('join/', JoinCompetitionView.as_view(), name='join-competition'),
<<<<<<< HEAD
    # path('submit/', SumbitCodeView.as_view(), name='submit-code'),
    # path('results/', StatisticsAPIVIew.as_view(), name='statistics' )
=======
    path('submit/', SubmitCodeView.as_view(), name='submit-code'),
    path('results/', StatisticsAPIView.as_view(), name='statistics' )
>>>>>>> origin/main
]
