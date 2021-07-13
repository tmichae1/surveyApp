from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_survey, name='create'),
    path('create/section/<url_id>/', views.add_section, name="add-section"),
    path('survey/<url_id>/<token>/', views.take_questionnaire, name='take-survey'),
    path('survey/success/', views.questionnaire_taken, name='survey-taken'),
    path('survey/post/', views.send_questionnaire, name='send-survey'),
    path('surveys/status/', views.survey_status, name='survey-status'),
    path('surveys/delete/<url_id>/', views.delete_survey, name='delete-survey'),
    path('survey/<url_id>/info/edit/', views.edit_survey_info, name='edit-survey-info')
]