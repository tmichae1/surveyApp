from django.shortcuts import render, redirect, get_object_or_404
from.models import Survey, Question, SurveyToken, Email, Answer
from django.contrib import messages
import random, string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from survay import settings
from .functions import create_questions
from .forms import EditSurveyInfoForm
import datetime



# Create your views here.
@login_required
def home(request):
    template_name = "questionnaire/main.html"
    # Get surveys
    




    return render(request, template_name)

@login_required
def create_survey(request):
    template_name = "questionnaire/create.html"
    input_range = [1,2,3,4,5,6,7,8,9,10]
    if request.method == "POST":
        if "add_section" in request.POST:
            # get name of questionnaire
            name = request.POST['title']

            # create questionnaire model instance
            url_id = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            survey = Survey(name=name, url_id=url_id, created_by=request.user)
            survey.save()
            # Create questions
            create_questions(request, survey)
            messages.success(request, "Section Added.")
            return redirect("add-section", url_id=url_id)
        else:
            # get name of questionnaire
            name = request.POST['title']

            # create questionnaire model instance
            url_id = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            survey = Survey(name=name, url_id=url_id, created_by=request.user)
            survey.save()
            # Create questions
            create_questions(request, survey)
            messages.success(request, "Survey Created.")
            return redirect("home")
    context = {
        "input_range": input_range
    }
    return render(request, template_name, context)

@login_required
def add_section(request, url_id):
    template_name = "questionnaire/add_section.html"
    input_range = [1,2,3,4,5,6,7,8,9,10]
    # get questionnaire with url id
    survey = get_object_or_404(Survey, url_id=url_id)

    # handle post request
    if request.method == "POST":
        # check which submit button was pressed
        if "add_section" in request.POST:
            # create questions
            create_questions(request, survey)
            messages.success(request, "Section Added.")
            return redirect("add-section", url_id=url_id)
        else:
            # create questions
            create_questions(request, survey)
            messages.success(request, "Survey Created.")
            return redirect("home")
    context = {
        "input_range": input_range,
        "survey_name": survey.name
    }
    return render(request, template_name, context)

def take_questionnaire(request, url_id, token):
    template_name = "questionnaire/survey.html"
    survey = get_object_or_404(Survey, url_id=url_id)
    access = get_object_or_404(SurveyToken, token=token, survey=survey)
    # Check questionnaire exists and the participant token matches
    if request.method == "POST":
        # get list of questions
        access.taken = True
        access.save()
        questions = Question.objects.filter(survey=survey)
        for question in questions:
            question_answer = request.POST["{0}_{1}".format(question.category, question.question)]
            print(question_answer)
            answer = Answer(question=question, answer=question_answer, survey_token = access)
            answer.save()
        return redirect("survey-taken")

    #   change survey expired to false if not already
    if survey.expired is True:
        survey.expired = True
        survey.save()
        expired = True
    else:
        expired = False

    # Check if survey link has already been used
    if access.taken is True:
        taken = True
    else:
        taken = False

    # get questions and question categories
    questions = Question.objects.filter(survey=survey)
    categroies = Question.objects.filter(survey=survey).values("category").distinct()

    question_list = list()
    for c in categroies:
        # Create a list of questions to pass to the html. Format [{"category": "category name", "questions": []}]
        section_dict = {"name": c["category"], "questions": list()}
        question_list.append(section_dict)

    for section in question_list:
        for question in questions:
            # assign qiestion to correct category
            if question.category == section["name"]:
                new_question = dict()
                new_question["question"] = question.question
                new_question["question_type"] = question.question_type
                new_question["answers"] = list()
                if new_question["question_type"] == "Multiple Choice":
                    answers = question.question_answers.split("/")
                    for answer in answers:
                        new_question["answers"].append(answer)
                section["questions"].append(new_question)
    context = {"survey": survey,
               "question_list": question_list,
               "taken": taken,
               "expired": expired}
    return render(request, template_name, context)

def questionnaire_taken(request):
    template_name = "questionnaire/survey_taken.html"
    return render(request, template_name)

@login_required
def send_questionnaire(request):
    template_name="questionnaire/post_survey.html"
    surveys = Survey.objects.filter(created_by=request.user)
    if request.method == "POST":
        survey_id = int(request.POST["survey"])
        date_picker = request.POST["date-picker"]
        survey = Survey.objects.filter(id=survey_id).first()
        expiry_date = datetime.datetime.strptime(date_picker, "%Y-%m-%d")
        survey.expiry_date = expiry_date
        survey.save()
        emails = Email.objects.all()
        for email in emails:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            surveyToken = SurveyToken(token=token, survey=survey)
            surveyToken.save()
            message = "Here is your personal link. \n" \
                      "http://127.0.0.1:8000/survey/{0}/{1}".format(survey.url_id, token)
            send_mail(
                'Please Can You Take this New Survey',
                message,
                settings.EMAIL_HOST_USER,
                [email.email]
            )
        messages.success(request, "Questionnaire Posted")
        return redirect('home')
    context = {"surveys": surveys}
    return render(request, template_name, context)

def survey_status(request):
    template_name = "questionnaire/survey_status.html"
    # Get all surveys created by the user
    surveys = Survey.objects.filter(created_by=request.user)
    # create a list to hold survey information
    list_of_surveys = list()
    for survey in surveys:
        survey_dict = dict()
        survey_dict["url_id"] = survey.url_id
        survey_dict["name"] = survey.name
        #   Check the status of the survey and adjust element accordingly
        survey_expiry = survey.expiry_date
        if survey_expiry is None:
            survey_dict["status"] = "Not Yet Published"
        elif survey.expired:
            survey_dict["status"] = "Expired"
        else:
            survey_dict["status"] = "{0}".format(survey.expiry_date.strftime("%d/%m/%Y"))
        # see how many survey token were created
        num_tokens = len(SurveyToken.objects.filter(survey=survey))
        # if survey has expiry date, calculate values
        if survey_expiry:
            survey_dict["published"] = num_tokens
            # see how many tokens have been taken
            num_completed = len(SurveyToken.objects.filter(survey=survey, taken=True))
            survey_dict["surveys_completed"] = num_completed
            # minus num_completed from num_tokens to get total surveys not taken
            survey_dict["surveys_not_completed"] = num_tokens - num_completed
        # if not, values will equal n/a
        else:
            survey_dict["published"] = "N/A"
            survey_dict["surveys_completed"] = "N/A"
            survey_dict["surveys_not_completed"] = "N/A"
        list_of_surveys.append(survey_dict)
    context = {"surveys": list_of_surveys}
    return render(request, template_name, context)


@login_required
def delete_survey(request, url_id):
    survey = get_object_or_404(Survey, url_id=url_id, created_by=request.user)
    survey.delete()
    return redirect("survey-status")


def edit_survey_info(request, url_id):
    template_name = "questionnaire/edit_survey_info.html"
    survey = get_object_or_404(Survey, url_id=url_id, created_by=request.user)
    if request.method == "POST":
        form = EditSurveyInfoForm(request.POST)
        if form.is_valid():
            survey.name = form.instance.name
            survey.expiry_date = form.instance.expiry_date
            survey.save()
            return redirect("survey-status")
    else:
        form = EditSurveyInfoForm(instance=survey)
    context={"form": form}

    return render(request, template_name, context)

