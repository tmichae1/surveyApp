from . models import Question

def create_questions(request, survey):
    # get section_name
    section_name = request.POST['section-name']

    # Filter through question inputs and remove blanks
    questions = request.POST.getlist('question')
    question_types = request.POST.getlist('question_type')
    answer_types = request.POST.getlist('answers')
    questions_filtered = []
    for i in range(0, len(questions)):
        if questions[i].replace(" ", "") != "":
            new_question = dict()
            # Get question title
            # Strip Question title of special characters
            title = questions[i]
            title = title.replace("’", "'").replace(",", ",")
            # Add stripped title to dict
            new_question["question"] = title
            # Get The answer type of the question (Multiple Choice, true/false etc)
            new_question["question_type"] = question_types[i]
            # If answer type is multiple choice, format the answer to ("answer1/answer2/answer3....")
            if new_question["question_type"] == "Multiple Choice":
                answers = answer_types[i].split("/")
                formatted_answer = ""
                for answer in answers:
                    answer = answer.lstrip()
                    answer = answer.rstrip()
                    formatted_answer += "{0}/".format(answer)
                formatted_answer = formatted_answer.rstrip("/")
            # If answer type is not multiple choice. assign none
            else:
                formatted_answer = None

            new_question["answers"] = formatted_answer
            # Append to list of question
            questions_filtered.append(new_question)

    # Create Questions model instance
    for question in questions_filtered:
        if question["answers"] is not None:
            new_question = Question(survey=survey, question=question["question"],
                                    question_type=question["question_type"],
                                    question_answers=question["answers"],
                                    category=section_name)
            new_question.save()
        else:
            new_question = Question(survey=survey, question=question["question"],
                                    question_type=question["question_type"],
                                    category=section_name)
            new_question.save()
