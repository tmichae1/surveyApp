from django.contrib import admin
from .models import SurveyToken, Question, Survey, Email, Answer
# Register your models here.
admin.site.register(SurveyToken)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Email)
admin.site.register(Answer)
