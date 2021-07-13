from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Survey(models.Model):
    name = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id = models.CharField(max_length=15, unique=True)
    expiry_date = models.DateField(null=True)
    expired = models.BooleanField(default=False)
    answers_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SurveyToken(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    token = models.CharField(max_length=15, unique=True)
    taken = models.BooleanField(default=False)


    def __str__(self):
        status = ""
        if self.taken:
            status = "Taken"
        else:
            status = "Not Taken"
        return self.token


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=50)
    question_answers = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.question, self.survey.name, self.category)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=500, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    survey_token = models.ForeignKey(SurveyToken, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.answer, self.question)


class Email(models.Model):
    email = models.EmailField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.email
