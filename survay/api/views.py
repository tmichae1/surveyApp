from django.shortcuts import render
from rest_framework.decorators import api_view
from questionnaire.models import Survey, Question
from.serializer import QuestionnaireSerializer
from rest_framework.response import Response
import random, string
from django.http import HttpResponse, JsonResponse

# Create your views here.
@api_view(['POST'])
def create_questionaire(request):
    questionnaire_data = request.data
    print(questionnaire_data["name"])
    url_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    questionnaire = Survey(name=questionnaire_data["name"], url_id=url_id)
    questionnaire.save()
    questions = questionnaire_data["questions"]
    for i in questions:
        question = Question(questionnaire=questionnaire, question=i["question"])
        question.save()
    serializer = QuestionnaireSerializer(questionnaire_data)
    return Response(serializer.data)
