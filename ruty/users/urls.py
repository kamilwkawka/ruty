from django.urls import path
from .views import RegisterUserView, UpdateProfileView, SurveyResponseView, UserGroupView, MessageListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', UpdateProfileView.as_view(), name='profile'),
    path('survey/', SurveyResponseView.as_view(), name='survey'),
    path('group/', UserGroupView.as_view(), name='user-group'),
    path('group/<int:group_id>/messages/', MessageListView.as_view(), name='group-messages')
]