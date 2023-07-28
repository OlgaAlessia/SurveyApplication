from flask import Flask, render_template, request, flash, redirect
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

KEY_RESPONSES = "responses"
KEY_SURVEY_ID = 'current_survey'

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret40"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def get_surveys():
    
    """Show list of survey"""
    return render_template("select-survey.html", surveys = surveys)

@app.route('/start_survey', methods=["POST"])
def get_user_survey():
    """Show list of survey"""
    
    survey_id = request.form['survey_id']
    session[KEY_SURVEY_ID] = survey_id
    survey = surveys[survey_id]
    
    complited = request.cookies.get(f"complite_{survey_id}")
    if complited == "true":
        flash(f"The {survey_id.capitalize()} Survey was Complited.")
        return redirect("/complete_2")
        
    session[KEY_RESPONSES] = []
    
    return render_template("start-survey.html", survey = survey)


@app.route('/questions/<int:number>')
def get_question(number):
    """Show the question"""
    
    survey_id = session[KEY_SURVEY_ID] 
    responses = session[KEY_RESPONSES]
    survey = surveys[survey_id]
    
    if number > len(responses):
        flash(f"Try to access an invalid question {number}.")
        return redirect(f'/questions/{len(responses)}')
    
    if (len(responses) == len(survey.questions)):
        # The user answered all the questions!
        return redirect("/complete")
    
    if number != len(responses):
        flash(f"Try to access an invalid question {number}.")
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[number]
    return render_template("questions.html", qid=number, question=question)

@app.route('/answer', methods=["POST"])
def get_answer():
    """Get the answer of the question"""

    if request.form.get('text'):
        answer = request.form['choice'] + ' ' + request.form.get('text')
    else:
        answer = request.form['choice'] 

    survey_id = session[KEY_SURVEY_ID]
    
    #getting the [] from session, adding the answer and restore the new []
    responses = session[KEY_RESPONSES]
    responses.append(answer)
    session[KEY_RESPONSES] = responses


    if (len(responses) == len(surveys[survey_id].questions)):
        # The user answered all the questions!
        return redirect("/complete")
    
    return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def show_thanks():
    """Survey Complited. Show Thank you page with survey answers"""
    
    survey_id = session[KEY_SURVEY_ID] 

    html =  render_template('complete.html', 
                            survey=surveys[survey_id], 
                            responses=session[KEY_RESPONSES])

    resp = make_response(html)
    
    resp.set_cookie(f"complite_{survey_id}", "true")
    
    return resp

@app.route('/complete_2')
def complited():
    """Survey Complited and "complite" in cookie = true Show a Thank you Page"""
    
    survey_id = session[KEY_SURVEY_ID] 
    survey = surveys[survey_id]
    
    return render_template("complete-2.html", survey=survey)
    