from django.urls import path, include
from . import views

urlpatterns = [
    path("create-questionnaire/", views.create_questionaire, name="create-questionnaire")
]