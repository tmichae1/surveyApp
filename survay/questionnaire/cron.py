from . models import Survey, Question, SurveyToken, Answer
from django.core.mail.message import EmailMessage
from survay import settings
import datetime
import csv
import os



# Cron job to check expiry date of surveys
def expired_check():
    surveys = Survey.objects.exclude(expiry_date__isnull = True)
    today = datetime.date.today()
    for survey in surveys:
        if not survey.expired:
            if today >= survey.expiry_date:
                survey.expired = True
                survey.save()


def email_results():
    # Get surveys that have expired and have not had answers emailed
    surveys = Survey.objects.filter(expired=True, answers_sent=False)
    for survey in surveys:
        # get survey tokens and sections
        survey_tokens = SurveyToken.objects.filter(survey=survey)
        sections = Question.objects.filter(survey=survey).values("category").distinct()
        # Check to see if at least one person answered the surveys
        num_completed = len(SurveyToken.objects.filter(survey=survey, taken=True))
        counter = 1
        if num_completed > 0:
            with open("{0}.csv".format(survey.name), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([survey.name])
                for section in sections:
                    # Get section name
                    section_name = section['category']
                    # Write section name in csv file
                    writer.writerow(["section {0} - {1}".format(counter, section_name)])
                    counter += 1

                    # Get all questions in section
                    questions = Question.objects.filter(survey=survey, category=section_name)
                    # put all question titles in a list
                    question_list = list()
                    question_list.append("Questions")
                    for question in questions:
                        question_list.append(question.question)
                    # write questions to the csv file
                    writer.writerow(question_list)

                    #loop through tokens to get answer for particular section
                    for token in survey_tokens:
                        if token.taken is True:
                            # Create answers list and append answer strings
                            answers = list()
                            answers.append("Answers")
                            for question in questions:
                                answer = Answer.objects.filter(survey_token=token, question=question).first()
                                answers.append(answer.answer)
                            # Write answers in csv file
                            writer.writerow(answers)
            with open("{0}.csv".format(survey.name), "r") as f:
                receiver = survey.created_by.email
                print(receiver)
                message = 'Here is the answers for survey - {0}'.format(survey.name)
                email = EmailMessage('Survey - {0} answers'.format(survey.name),
                                     message,
                                     settings.EMAIL_HOST_USER,
                                     [receiver])
                email.attach("{0}.csv".format(survey.name), f.read(), 'text/csv')
                email.send()
            os.remove("{0}.csv".format(survey.name))
        survey.answers_sent = True
        survey.save()
